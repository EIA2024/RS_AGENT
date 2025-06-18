RS_AGENT/
├── .env # 环境变量配置文件（需手动创建，存放API密钥等敏感信息）
├── .gitignore # Git忽略文件
├── main.py # 主程序入口，命令行交互与测试
├── agent.py # 任务分发与核心调度
│
├── core/
│ ├── init.py
│ └── config.py # 全局配置与LLM初始化
│
├── handlers/
│ ├── init.py
│ ├── instruction_0.py # 任务意图识别
│ └── instruction_1.py # 交互式知识库问答
│
├── utils/
│ ├── init.py
│ ├── file_handler.py # 文件读取工具
│ ├── knowledge_base.py# 知识库实现（模拟、本地文件、API）
│ └── parsers.py # LLM输出解析工具
│
├── requirements.txt # 依赖包列表
└── test_knowledge_base.py # 知识库功能测试脚本

---

## 🚀 使用方法

1. **克隆项目**
   ```bash
   git clone https://github.com/EIA2024/RS_AGENT.git
   cd RS_AGENT
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **配置环境变量**
   - 在项目根目录下新建 `.env` 文件，内容如下（请填写你的API Key）：
     ```
     ARK_API_KEY=your_api_key_here
     VOLCANO_MODEL_NAME=deepseek-v3-250324
     KNOWLEDGE_BASE_PATH=./knowledge_base
     KNOWLEDGE_BASE_INDEX_PATH=./knowledge_base/index
     OUTPUT_DIR=./output
     ```

4. **运行主程序**
   - 命令行交互模式：
     ```bash
     python main.py
     ```
   - 或直接传入问题：
     ```bash
     python main.py --query "土壤湿度是什么？"
     ```

5. **运行测试脚本**
   ```bash
   python test_knowledge_base.py
   ```

---

## ⚙️ 配置说明

- `.env` 文件用于存放敏感信息和路径配置，**不会被提交到Git仓库**。
- 主要环境变量说明：
  - `ARK_API_KEY`：火山引擎API密钥（必填）
  - `VOLCANO_MODEL_NAME`：大模型名称（可选，默认已设）
  - `KNOWLEDGE_BASE_PATH`：知识库文件夹路径
  - `KNOWLEDGE_BASE_INDEX_PATH`：知识库索引路径
  - `OUTPUT_DIR`：输出文件夹路径

---

## 📚 主要功能

- 支持遥感领域术语的智能问答与澄清
- 支持本地/模拟/远程API三种知识库模式
- 可扩展的 LLM 接入与多任务分发
- 交互式命令行体验

---

## 📝 备注

- `.env` 文件需手动创建并正确填写API密钥
- 如需使用远程LLM推理，必须配置有效的API Key
- 详细开发文档与二次开发接口请参考各模块源码注释

---

如有问题欢迎提issue或联系作者！

