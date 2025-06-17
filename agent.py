from typing import List, Any
from utils.file_handler import read_files_to_string
from handlers.instruction_0 import handle_instruction_0
from handlers.instruction_1 import handle_instruction_1_interactive

def run_analysis_agent(instruction: int, prompt: str, file_paths: List[str] = None, output_path: str = None) -> Any:
    """
    RS Agent's main entry point, dispatching tasks to appropriate handlers.
    """
    file_content = read_files_to_string(file_paths)

    if instruction == 0:
        # Call the handler for instruction 0
        return handle_instruction_0(prompt, file_content)
    
    elif instruction == 1:
        if not output_path:
            print("[错误] instruction 1 需要提供 output_path。")
            return -1
        # Call the handler for instruction 1
        success = handle_instruction_1_interactive(prompt, file_content, output_path)
        return 0 if success else -1
        
    elif instruction in [2, 3]:
        print(f"[Agent] instruction {instruction} 尚未实现。")
        return -1
        
    else:
        print(f"[错误] 未知的 instruction: {instruction}")
        return -1

def process_user_query(prompt: str, file_paths: List[str] = None, output_path: str = None) -> Any:
    """
    处理用户查询的主函数。
    首先进行意图分类，然后根据分类结果进行相应处理。
    """
    # 第一步：意图分类
    task_id = handle_instruction_0(prompt, read_files_to_string(file_paths))
    
    if task_id == -2:
        # 如果是可纠正的模糊查询，直接进入交互式问答
        if not output_path:
            print("[错误] 需要提供 output_path 用于保存结果。")
            return -1
        success = handle_instruction_1_interactive(prompt, read_files_to_string(file_paths), output_path)
        return 0 if success else -1
    elif task_id < 0:
        # 如果是完全无关的查询，直接返回
        return task_id
    else:
        # 如果是标准任务，调用相应的处理器
        return run_analysis_agent(task_id, prompt, file_paths, output_path) 