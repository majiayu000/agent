from utils.log import Log, log_time
from typing import List, Any, Union
from core.agent_manager import AgentManager
from core.memory_system import MemorySystem
from core.tool_manager import ToolManager
from core.task_scheduler import TaskScheduler
from core.communication_hub import CommunicationHub
from core.monitoring_service import MonitoringService
from ui_automation.ui_driver import UIDriver
from ui_automation.vision_model import VisionModel
from config.settings import LOG_DIR, SERVICE_NAME
import ast

logger = Log.log(file_name="main", dir_name=LOG_DIR)


@log_time(logger)
def main() -> None:
    agent_manager = AgentManager()
    memory_system = MemorySystem()
    tool_manager = ToolManager()
    task_scheduler = TaskScheduler(agent_manager)
    communication_hub = CommunicationHub()
    monitoring_service = MonitoringService()

    # 创建UI驱动和Vision Model
    ui_driver = UIDriver()
    vision_model = VisionModel()

    # 创建UITestAgent
    ui_test_agent = agent_manager.create_agent(
        "UITestAgent",
        {
            "memory": memory_system,
            "tools": tool_manager.get_all_tools(),
            "ui_driver": ui_driver,
            "vision_model": vision_model,
            "test_cases": ["login_test", "search_test", "checkout_test"],
        },
    )

    # 执行UI测试任务
    result = ui_test_agent.execute_task("run_all_tests")
    logger.info(f"UI tests completed with result: {result}")

    # 示例:执行特定操作
    action_result = ui_test_agent.execute_task("execute_action:touch,0.5,0.5")
    logger.info(f"Action executed with result: {action_result}")

    # 示例:分析屏幕
    screenshot = ui_driver.take_screenshot()
    logger.info(f"main.py 中的 screenshot: {screenshot}")
    analysis_result = ui_test_agent.execute_task(f"analyze_screen:{screenshot}")
    logger.info(f"Screen analysis result: {analysis_result}")

    logger.info("UI testing completed.")


if __name__ == "__main__":
    main()
