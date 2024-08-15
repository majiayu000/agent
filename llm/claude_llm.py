from .base_llm import BaseLLM
from typing import List, Dict, Any
from anthropic import Anthropic


class ClaudeLLM(BaseLLM):
    def __init__(self, api_key: str, model: str):
        self.client = Anthropic(api_key=api_key)
        self.model = model

    def generate_response(self, messages: List[Dict[str, str]]) -> str:
        response = self.client.messages.create(model=self.model, messages=messages)
        return response.content

    def analyze_image(self, image_path: str, prompt: str) -> str:
        with open(image_path, "rb") as image_file:
            response = self.client.messages.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "data": base64.b64encode(image_file.read()).decode(
                                        "utf-8"
                                    ),
                                },
                            },
                        ],
                    }
                ],
            )
        return response.content
