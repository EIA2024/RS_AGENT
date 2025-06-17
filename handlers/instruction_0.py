from langchain_core.prompts import ChatPromptTemplate
from core.config import LLM, KNOWN_TECHNICAL_TERMS  # 导入已知术语列表
from utils.parsers import parse_last_line_as_int

def handle_instruction_0(user_prompt: str, file_content: str) -> int:
    """Handles instruction 0: Classifies the user's intent."""
    print("\n[Agent] 执行 instruction 0: 任务意图识别...")
    
    # 构建系统提示词，增加对模糊查询和无关查询的区分
    system_prompt = """
    你是一个智能任务分类助手。你的任务是分析用户的请求，并将其归类为以下几种情况：

    1. 标准任务类型（返回对应编号）：
       1: 用户询问遥感领域知识（例如"什么是土壤湿度？"或"RSHub怎么用？"）
       2: 用户希望根据参数构建环境（例如"帮我用这些参数模拟一下场景"）
       3: 用户希望根据环境数据推断参数（例如"看看这个数据对应的土壤参数是什么"）

    2. 可纠正的模糊查询（返回-2）：
       - 用户使用了与标准术语相近但不完全匹配的词语
       - 例如："土地湿度"（应为"土壤湿度"）、"微波传感器"（应为"微波遥感"）
       - 这类查询可以通过提供标准术语建议来纠正

    3. 完全无关的查询（返回-1）：
       - 与遥感领域完全无关的问题
       - 例如："今天星期几？"、"帮我写个作文"等
       - 这类查询应该被拒绝

    已知的标准技术术语列表：
    {known_terms}

    请严格按照以下规则判断：
    1. 如果用户的请求完全匹配某个标准任务类型，返回对应的编号（1-3）
    2. 如果用户的请求使用了模糊或相近的术语，但明显是在询问遥感领域的问题，返回-2
    3. 如果用户的请求与遥感领域完全无关，返回-1

    请在你的回答最后一行单独输出判断结果（1、2、3、-1或-2）。
    """
    
    # 构建完整提示词
    full_prompt = f"用户请求：\n{user_prompt}\n\n"
    if file_content:
        full_prompt += f"用户上传的文件内容：\n{file_content}"
    
    # 创建提示模板
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", system_prompt.format(known_terms=str(KNOWN_TECHNICAL_TERMS))),
        ("user", "{input}")
    ])
    
    # 构建处理链
    chain = prompt_template | LLM
    
    try:
        # 调用LLM
        response = chain.invoke({"input": full_prompt})
        llm_output = response.content
        print(f"[LLM Output for Inst 0]\n{llm_output}")
        
        # 解析结果
        task_id = parse_last_line_as_int(llm_output)
        
        # 根据结果类型输出不同的提示信息
        if task_id > 0:
            print(f"[Agent] 识别到标准任务，任务ID: {task_id}")
        elif task_id == -2:
            print("[Agent] 识别到可纠正的模糊查询")
        else:
            print("[Agent] 识别到无关查询，拒绝处理")
            
        return task_id
        
    except Exception as e:
        print(f"[错误] 调用LLM时发生错误: {e}")
        return -1 