from zhipuai import ZhipuAI
from ..api_key import APIKeyManager
from ..config import ChatGLM_API_KEY_PATH
import warnings
import json


class ChatGLMClient:

    def __init__(self):
        self.api_key_manager = APIKeyManager(ChatGLM_API_KEY_PATH)
        self.api_key = self.api_key_manager.load_api_key()

        if self.api_key is None:
            warnings.warn("ChatGLM API key not found. Please provide an API key.")
            self.api_key = self.input_api_key()
            self.api_key_manager.save_api_key(self.api_key)

        self.client = ZhipuAI(api_key=self.api_key)
        self.system_prompt = "You are a helpful assistant."

    def set_system_prompt(self, prompt):
        self.system_prompt = prompt

    def chat(self, prompt):
        return self.from_json(self.client.chat.completions.create(
            model='GLM-4-AirX',
            messages=[
                {
                    "role": "system",
                    "content": self.system_prompt
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
        ).choices[0].message.content)

    @staticmethod
    def input_api_key():
        return input("Please enter your ChatGLM API key: ")

    @staticmethod
    def from_json(json_data):
        try:
            return json.loads(json_data)
        except:
            raise ValueError("Invalid JSON format.")
