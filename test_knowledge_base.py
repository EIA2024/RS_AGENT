import os
import json
from utils.knowledge_base import (
    query_knowledge_base,
    set_knowledge_base,
    MockKnowledgeBase,
    FileKnowledgeBase
)

def test_mock_knowledge_base():
    """测试模拟知识库"""
    print("\n" + "="*50)
    print("测试场景1：模拟知识库")
    print("="*50)
    
    # 测试默认知识库
    print("\n[测试] 使用默认知识库")
    result = query_knowledge_base([("土壤湿度", 1.0)])
    print(f"查询结果: {result}")
    
    # 测试自定义知识库
    print("\n[测试] 使用自定义知识库")
    custom_data = {
        "新术语1": "这是新知识1的内容",
        "新术语2": "这是新知识2的内容"
    }
    set_knowledge_base('mock', knowledge_data=custom_data)
    result = query_knowledge_base([("新术语1", 1.0)])
    print(f"查询结果: {result}")

def test_file_knowledge_base():
    """测试文件知识库"""
    print("\n" + "="*50)
    print("测试场景2：文件知识库")
    print("="*50)
    
    # 创建测试知识库文件
    test_data = {
        "文件术语1": "这是文件知识库中的内容1",
        "文件术语2": "这是文件知识库中的内容2"
    }
    test_file = "test_knowledge.json"
    
    try:
        # 写入测试数据
        with open(test_file, 'w', encoding='utf-8') as f:
            json.dump(test_data, f, ensure_ascii=False, indent=2)
        
        # 测试文件知识库
        print("\n[测试] 使用文件知识库")
        set_knowledge_base('file', file_path=test_file)
        result = query_knowledge_base([("文件术语1", 1.0)])
        print(f"查询结果: {result}")
        
    finally:
        # 清理测试文件
        if os.path.exists(test_file):
            os.remove(test_file)

def test_error_handling():
    """测试错误处理"""
    print("\n" + "="*50)
    print("测试场景3：错误处理")
    print("="*50)
    
    # 测试不存在的术语
    print("\n[测试] 查询不存在的术语")
    result = query_knowledge_base([("不存在的术语", 1.0)])
    print(f"查询结果: {result}")
    
    # 测试空关键词列表
    print("\n[测试] 空关键词列表")
    result = query_knowledge_base([])
    print(f"查询结果: {result}")

def main():
    """运行所有测试"""
    print("开始知识库测试...")
    
    # 运行测试场景
    test_mock_knowledge_base()
    test_file_knowledge_base()
    test_error_handling()
    
    print("\n知识库测试完成！")

if __name__ == "__main__":
    main() 