from .base_llm import BaseLLM
from typing import List, Dict, Any
import requests


class DeepSeekLLM(BaseLLM):
    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model
        self.api_url = "https://api.deepseek.com/v1/chat/completions"  # 假设的API端点

    def generate_response(self, messages: List[Dict[str, str]]) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        data = {"model": self.model, "messages": messages}
        response = requests.post(self.api_url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

    def analyze_image(self, image_path: str, prompt: str) -> str:
        # 假设DeepSeek不支持直接的图像分析,我们可以返回一个提示信息
        return "Image analysis is not supported by DeepSeek LLM."
