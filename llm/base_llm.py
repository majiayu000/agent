from abc import ABC, abstractmethod
from typing import List, Dict, Any


class BaseLLM(ABC):
    @abstractmethod
    def generate_response(self, messages: List[Dict[str, str]]) -> str:
        pass

    @abstractmethod
    def analyze_image(self, image_path: str, prompt: str) -> str:
        pass
