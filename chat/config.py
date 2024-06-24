import os

# 子目录CHAT路径
CHAT_DIR = os.path.dirname(os.path.abspath(__file__))

# 密钥路径
KEY_PATH = os.path.join(CHAT_DIR, 'api_key', '.key')

# ChatGLM_API_KEY
ChatGLM_API_KEY_PATH = os.path.join(CHAT_DIR, 'api_key', '.chatglm_api_key_cache')

