RS_AGENT/
├── .env                 # Your environment variables (API Key)
├── main.py              # Main entry point for testing and demonstration
├── agent.py             # The main agent dispatcher function (run_analysis_agent)
│
├── core/
│   ├── __init__.py      # Makes 'core' a Python package
│   └── config.py        # Central configuration: LLM initialization, constants
│
├── handlers/
│   ├── __init__.py      # Makes 'handlers' a Python package
│   ├── instruction_0.py # Logic for instruction 0 (intent classification)
│   └── instruction_1.py # Logic for instruction 1 (interactive QA)
│
└── utils/
    ├── __init__.py      # Makes 'utils' a Python package
    ├── file_handler.py  # File reading utilities
    ├── knowledge_base.py# Simulated knowledge base access
    └── parsers.py       # Helper functions for parsing LLM output

1.OpenAI API配置:
ARK_API_KEY=your_api_key_here
BASE_URL=https://ark.cn-beijing.volces.com/api/v3
VOLCANO_MODEL_NAME=deepseek-v3-250324


2.知识库配置：
KNOWLEDGE_BASE_PATH=./knowledge_base
KNOWLEDGE_BASE_INDEX_PATH=./knowledge_base/index

3.日志配置：
LOG_LEVEL=INFO
LOG_FILE=./logs/agent.log

4.系统配置：
SYSTEM_NAME=RS_AGENT
SYSTEM_VERSION=1.0.0
SYSTEM_DESCRIPTION=基于知识库的智能问答系统

