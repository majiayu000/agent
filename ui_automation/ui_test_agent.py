from typing import Dict, Any, List
from agents.base_agent import Agent
from utils.log import Log, log_time
from config.settings import LOG_DIR, SCREENSHOT_DIR
from ui_automation.ui_driver import UIDriver
from ui_automation.vision_model import VisionModel

logger = Log.log(file_name="ui_test_agent", dir_name=LOG_DIR)


class UITestAgent(Agent):
    def __init__(self, agent_id: str, config: Dict[str, Any]):
        super().__init__(agent_id, config)
        self.ui_driver: UIDriver = config.get("ui_driver")
        self.vision_model: VisionModel = config.get("vision_model")
        self.test_cases: List[str] = config.get("test_cases", [])

    @log_time(logger)
    def execute_task(self, task: str) -> Any:
        if task.startswith("analyze_screen:"):
            # 直接传递 screenshot 字典，而不是字符串
            screenshot = task.split("analyze_screen:", 1)[1]
            return self.analyze_screen(eval(screenshot))
        elif task == "run_all_tests":
            return self.run_all_tests()
        elif task.startswith("run_test:"):
            test_name = task.split(":")[1]
            return self.run_single_test(test_name)
        elif task.startswith("execute_action:"):
            action_data = task.split(":", 1)[1]
            return self.execute_action(action_data)
        else:
            raise ValueError(f"Unknown task: {task}")

    def run_all_tests(self) -> Dict[str, Any]:
        results = {}
        for test_case in self.test_cases:
            results[test_case] = self.run_single_test(test_case)
        return results

    def run_single_test(self, test_name: str) -> Any:
        logger.info(f"Running test: {test_name}")
        screenshot = self.ui_driver.take_screenshot()
        screen_analysis = self.analyze_screen(screenshot)
        # 根据screen_analysis执行操作
        return {"status": "success", "message": f"Test {test_name} completed"}

    def analyze_screen(self, screenshot: Dict[str, Any]) -> List[Dict[str, Any]]:
        logger.info(f"analyze_screen 接收到的 screenshot 类型: {type(screenshot)}")
        logger.info(f"analyze_screen 接收到的 screenshot 内容: {screenshot}")
        return self.vision_model.analyze_image(screenshot)

    def execute_action(self, action_data: str) -> Any:
        action_type, *params = action_data.split(",")
        if action_type == "touch":
            x, y = map(float, params)
            return self.ui_driver.touch(x, y)
        elif action_type == "back":
            return self.ui_driver.back()
        elif action_type == "type":
            text = ",".join(params)
            return self.ui_driver.type(text)
        elif action_type == "swipe":
            start_x, start_y, end_x, end_y = map(float, params)
            return self.ui_driver.swipe(start_x, start_y, end_x, end_y)
        else:
            logger.warning(f"Unknown action type: {action_type}")
            return None

    def add_test_case(self, test_case: str) -> None:
        self.test_cases.append(test_case)
        logger.info(f"Added new test case: {test_case}")

    def remove_test_case(self, test_case: str) -> None:
        if test_case in self.test_cases:
            self.test_cases.remove(test_case)
            logger.info(f"Removed test case: {test_case}")
        else:
            logger.warning(f"Test case not found: {test_case}")
