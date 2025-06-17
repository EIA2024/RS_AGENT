import os
from typing import List

def read_files_to_string(file_paths: List[str] = None) -> str:
    """Reads user-uploaded files and concatenates them into a single string."""
    if not file_paths:
        return ""
    
    content = []
    for path in file_paths:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content.append(f"--- 文件: {os.path.basename(path)} ---\n{f.read()}")
        except Exception as e:
            content.append(f"--- 无法读取文件: {os.path.basename(path)}, 错误: {e} ---")
    return "\n\n".join(content) 