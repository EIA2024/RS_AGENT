import os
import traceback
from typing import Optional, List
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from core.config import LLM, KNOWN_TECHNICAL_TERMS
from utils.knowledge_base import query_knowledge_base

class TermClarification(BaseModel):
    is_ambiguous: bool = Field(description="如果用户提问中的核心术语是模糊的或不在已知列表中，则为True；否则为False。")
    original_term: str = Field(description="从用户提问中识别出的原始核心术语。")
    corrected_term: Optional[str] = Field(description="如果is_ambiguous为False，这里是对应的标准术语。")
    suggestions: Optional[List[str]] = Field(description="如果is_ambiguous为True，这里是推荐给用户的标准术语列表。")

def handle_instruction_1_interactive(user_prompt: str, file_content: str, output_path: str) -> bool:
    """Handles instruction 1: Interactive knowledge Q&A with clarification."""
    print("\n[Agent] 执行 instruction 1: 知识库问答 (交互式澄清模式)...")
    
    clarification_parser = JsonOutputParser(pydantic_object=TermClarification)
    system_prompt_template = """
    你是一个微波遥感领域的专家助手。你的任务是帮助用户澄清他们模糊的提问。
    已知的标准技术术语列表为: {known_terms}
    请分析用户的提问，并遵循以下规则：
    1. 识别用户提问中的核心技术术语。
    2. 将该术语与已知的标准技术术语列表进行比对。
    3. 如果用户的术语是标准术语之一，或者是非常明确的同义词（例如"RSHub使用" -> "RSHub"），请判定为不模糊。
    4. 如果用户的术语是模糊的、有错别字或不在列表中（例如"土地湿度"），请判定为模糊，并从标准列表中提供最相关的2-3个建议。
    5. 如果用户提供了之前的澄清上下文，请优先在上次建议的范围内进行判断。
    你必须严格按照指定的JSON格式进行输出，不要添加任何额外的解释。
    {format_instructions}
    """
    
    prompt_base = ChatPromptTemplate.from_messages([
        ("system", system_prompt_template),
        ("user", "{input}")
    ])
    
    prompt = prompt_base.partial(
        format_instructions=clarification_parser.get_format_instructions(),
        known_terms=str(KNOWN_TECHNICAL_TERMS)
    )

    clarification_chain = prompt | LLM | clarification_parser
    current_prompt = user_prompt
    clarification_context = ""

    # Clarification Loop
    while True:
        print("-" * 20)
        print(f"[Agent] 正在分析用户输入: '{current_prompt}'")
        full_clarification_prompt = (
            f"用户当前输入: '{current_prompt}'\n\n"
            f"历史澄清上下文:\n{clarification_context if clarification_context else '无'}"
        )

        try:
            clarification_result = clarification_chain.invoke({"input": full_clarification_prompt})
            
            if not clarification_result['is_ambiguous']:
                final_term = clarification_result['corrected_term']
                print(f"[Agent] 意图已澄清。识别出的标准术语为: '{final_term}'")
                break  # Exit loop
            else:
                suggestions = clarification_result['suggestions']
                original_term = clarification_result['original_term']
                print(f"\n[Agent] 您的提问 '{original_term}' 似乎有些模糊。")
                print("您是不是想询问以下某个概念？")
                for i, term in enumerate(suggestions):
                    print(f"  {i+1}. {term}")
                print("请直接输入您想查询的词语，或者输入序号，或输入'退出'来中止查询。")
                
                user_choice = input("您的选择: ").strip()

                if user_choice.lower() in ['退出', 'exit', 'quit']:
                    print("[Agent] 用户中止查询。")
                    return False
                
                if user_choice.isdigit() and 1 <= int(user_choice) <= len(suggestions):
                    current_prompt = suggestions[int(user_choice) - 1]
                else:
                    current_prompt = user_choice
                
                clarification_context = f"上一轮识别到模糊词 '{original_term}', 提供了选项 {suggestions}, 用户选择了 '{current_prompt}'."

        except Exception as e:
            print(f"[错误] 在澄清步骤中调用LLM失败: {e}")
            traceback.print_exc()
            return False

    # After loop, query knowledge base
    try:
        print("[Agent] 步骤 2/3: 查询知识库...")
        knowledge_text = query_knowledge_base([(final_term, 1.0)])
        
        print("[Agent] 步骤 3/3: 写入文件...")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(knowledge_text)

        if "抱歉" not in knowledge_text:
            print(f"[Agent] 成功！结果已写入: {output_path}")
            return True
        else:
            print(f"[Agent] 知识库中无此信息，已将提示写入文件。")
            return False # Or True, depending on desired behavior for "not found"
            
    except Exception as e:
        print(f"[错误] 在查询知识库或写入文件时发生错误: {e}")
        return False 