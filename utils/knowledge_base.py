from typing import List, Tuple, Dict, Any, Optional
from abc import ABC, abstractmethod
import json
import os

class KnowledgeBase(ABC):
    """知识库基类，定义知识库接口"""
    
    @abstractmethod
    def query(self, keywords_with_weights: List[Tuple[str, float]]) -> str:
        """查询知识库的抽象方法"""
        pass

class MockKnowledgeBase(KnowledgeBase):
    """模拟知识库实现，用于测试和开发"""
    
    def __init__(self, knowledge_data: Optional[Dict[str, str]] = None):
        self.knowledge_data = knowledge_data or {
            "土壤湿度": "土壤湿度是影响微波后向散射系数的关键地表参数之一。通常，湿度越高，介电常数越大，导致更强的雷达回波信号。",
            "RSHub": "RSHub是一个集成了多种微波遥感模型的平台，用户可以通过Python脚本调用其工具链，进行正向模拟和数据分析。",
            "微波遥感": "微波遥感利用微波波段的电磁波来探测地表信息，其优势在于能够穿透云雾，实现全天时全天候观测。",
            "地表粗糙度": "地表粗糙度描述了地表面的起伏状况，是影响雷达信号散射方向和强度的另一个重要因素。",
        }
    
    def query(self, keywords_with_weights: List[Tuple[str, float]]) -> str:
        """查询模拟知识库"""
        print(f"[知识库] 正在查询关键词: {keywords_with_weights}")
        if keywords_with_weights:
            first_keyword = keywords_with_weights[0][0]
            return self.knowledge_data.get(first_keyword, "抱歉，关于您提到的知识，我的知识库中暂无相关信息。")
        return "抱歉，未能识别出有效查询关键词。"

class FileKnowledgeBase(KnowledgeBase):
    """基于文件的知识库实现"""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self._load_knowledge()
    
    def _load_knowledge(self):
        """从文件加载知识库数据"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                self.knowledge_data = json.load(f)
        except FileNotFoundError:
            print(f"[警告] 知识库文件 {self.file_path} 不存在，使用空知识库")
            self.knowledge_data = {}
        except json.JSONDecodeError:
            print(f"[警告] 知识库文件 {self.file_path} 格式错误，使用空知识库")
            self.knowledge_data = {}
    
    def query(self, keywords_with_weights: List[Tuple[str, float]]) -> str:
        """查询文件知识库"""
        print(f"[知识库] 正在查询关键词: {keywords_with_weights}")
        if keywords_with_weights:
            first_keyword = keywords_with_weights[0][0]
            return self.knowledge_data.get(first_keyword, "抱歉，关于您提到的知识，我的知识库中暂无相关信息。")
        return "抱歉，未能识别出有效查询关键词。"

class APIKnowledgeBase(KnowledgeBase):
    """基于API的知识库实现"""
    
    def __init__(self, api_url: str, api_key: Optional[str] = None):
        self.api_url = api_url
        self.api_key = api_key
    
    def query(self, keywords_with_weights: List[Tuple[str, float]]) -> str:
        """查询API知识库"""
        # TODO: 实现API调用逻辑
        print(f"[知识库] 正在通过API查询关键词: {keywords_with_weights}")
        return "API知识库功能尚未实现"

class KnowledgeBaseFactory:
    """知识库工厂类，用于创建不同类型的知识库实例"""
    
    @staticmethod
    def create_knowledge_base(kb_type: str, **kwargs) -> KnowledgeBase:
        """
        创建知识库实例
        
        Args:
            kb_type: 知识库类型，可选值：'mock', 'file', 'api'
            **kwargs: 创建知识库所需的参数
        
        Returns:
            KnowledgeBase: 知识库实例
        """
        if kb_type == 'mock':
            return MockKnowledgeBase(kwargs.get('knowledge_data'))
        elif kb_type == 'file':
            return FileKnowledgeBase(kwargs.get('file_path', 'knowledge_base.json'))
        elif kb_type == 'api':
            return APIKnowledgeBase(
                kwargs.get('api_url'),
                kwargs.get('api_key')
            )
        else:
            raise ValueError(f"未知的知识库类型: {kb_type}")

# 默认使用模拟知识库
_knowledge_base = MockKnowledgeBase()

def set_knowledge_base(kb_type: str, **kwargs):
    """设置全局知识库实例"""
    global _knowledge_base
    _knowledge_base = KnowledgeBaseFactory.create_knowledge_base(kb_type, **kwargs)

def query_knowledge_base(keywords_with_weights: List[Tuple[str, float]]) -> str:
    """查询知识库的全局函数"""
    return _knowledge_base.query(keywords_with_weights)

"""
#文件知识库
set_knowledge_base('file', file_path='my_knowledge.json')

#API知识库
set_knowledge_base('api', 
    api_url='https://api.example.com/knowledge',
    api_key='your_api_key'
)

#自定义的模拟数据
custom_data = {
    "新术语1": "新知识1",
    "新术语2": "新知识2"
}

set_knowledge_base('mock', knowledge_data=custom_data) 
"""