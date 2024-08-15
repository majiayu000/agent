from typing import List, Dict, Any, Union
from utils.log import Log, log_time
from config.settings import LOG_DIR, LLM_CONFIG
from llm.llm_factory import LLMFactory
import os
import ast

logger = Log.log(file_name="vision_model", dir_name=LOG_DIR)


class VisionModel:
    def __init__(self):
        llm_type = LLM_CONFIG["default_provider"]
        llm_config = LLM_CONFIG["providers"][llm_type]
        self.llm = LLMFactory.create_llm(llm_type, llm_config)

    @log_time(logger)
    def analyze_image(
        self, image_info: Union[str, Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        logger.info(f"接收到的 image_info 类型: {type(image_info)}")
        logger.info(f"接收到的 image_info 内容: {image_info}")

        if isinstance(image_info, str):
            try:
                image_info = ast.literal_eval(image_info)
            except:
                logger.error(f"无法将字符串解析为字典: {image_info}")

        if isinstance(image_info, dict):
            image_path = image_info.get("screen", "")
        else:
            raise ValueError(f"无效的 image_info 类型: {type(image_info)}")

        if not image_path:
            raise ValueError("图片路径为空")

        root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        full_image_path = os.path.join(root_path, "ui_automation", "log", image_path)

        prompt = "Analyze this UI screenshot and identify UI components with their relative coordinates."
        response = self.llm.analyze_image(full_image_path, prompt)
        return self._parse_response(response)

    @log_time(logger)
    def compare_colors(self, image_path: str, element_name: str) -> Dict[str, Any]:
        prompt = f"What is the color of the {element_name} element in this image?"
        response = self.llm.analyze_image(image_path, prompt)
        return self._parse_color_response(response)

    def _parse_response(self, content: str) -> List[Dict[str, Any]]:
        logger.info(f"AI响应内容: {content}")
        # 实现解析逻辑,将AI响应转换为组件列表
        return []

    def _parse_color_response(self, content: str) -> Dict[str, Any]:
        logger.info(f"AI响应内容: {content}")
        # 实现解析逻辑,将AI响应转换为颜色信息
        return {}
