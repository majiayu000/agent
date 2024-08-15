from .base_llm import BaseLLM
from .gpt_llm import GPTLLM
from .claude_llm import ClaudeLLM
from .deepseek_llm import DeepSeekLLM
from typing import Dict, Any


class LLMFactory:
    @staticmethod
    def create_llm(llm_type: str, config: Dict[str, Any]) -> BaseLLM:
        if llm_type == "gpt":
            return GPTLLM(config["api_key"], config["model"])
        elif llm_type == "claude":
            return ClaudeLLM(config["api_key"], config["model"])
        elif llm_type == "deepseek":
            return DeepSeekLLM(config["api_key"], config["model"])
        else:
            raise ValueError(f"Unsupported LLM type: {llm_type}")
