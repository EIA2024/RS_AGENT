import os
import sys
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# Load environment variables from .env file at the project root
load_dotenv()

# --- Central Configuration ---
VOLCANO_API_KEY_ENV_VAR = "ARK_API_KEY"
VOLCANO_BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"
VOLCANO_MODEL_NAME = os.getenv("VOLCANO_MODEL_NAME", "deepseek-v3-250324")

# --- Shared Constants ---
KNOWN_TECHNICAL_TERMS = ["土壤湿度", "RSHub", "微波遥感", "地表粗糙度", "植被指数", "后向散射系数"]

# --- Global LLM Instance ---
print("--- Initializing LLM instance ---")
if VOLCANO_API_KEY_ENV_VAR not in os.environ:
    raise ValueError(
        f"环境变量 {VOLCANO_API_KEY_ENV_VAR} 未设置。"
        "请在项目根目录的 .env 文件中设置。"
    )

try:
    LLM = ChatOpenAI(
        model=VOLCANO_MODEL_NAME,
        temperature=0,
        openai_api_key=os.environ[VOLCANO_API_KEY_ENV_VAR],
        base_url=VOLCANO_BASE_URL,
        request_timeout=60.0,
    )
    print(f"--- LLM ({VOLCANO_MODEL_NAME}) initialized successfully ---")
except Exception as e:
    print(f"--- LLM initialization FAILED: {e} ---")
    sys.exit(1) 