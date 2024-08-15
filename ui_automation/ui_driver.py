from typing import Tuple
from utils.log import Log, log_time
from config.settings import LOG_DIR
from airtest.core.api import *
from poco.drivers.ios import iosPoco
from airtest.cli.parser import cli_setup

logger = Log.log(file_name="ui_driver", dir_name=LOG_DIR)


class UIDriver:
    def __init__(self):
        if not cli_setup():
            auto_setup(
                __file__,
                logdir=True,
                devices=[
                    "ios:///http://127.0.0.1:8100",
                ],
            )
        self.poco = iosPoco()

    @log_time(logger)
    def take_screenshot(self) -> str:
        # 截图代码
        try:
            screenshot_result = snapshot()  # 实际的截图操作
            logger.info(f"截图完成，结果: {screenshot_result}")
            return screenshot_result
        except Exception as e:
            logger.error(f"截图过程中出错: {e}")
            return None

    @log_time(logger)
    def touch(self, x: float, y: float) -> None:
        device_width, device_height = device().get_current_resolution()
        touch((device_width * x, device_height * y))
        logger.info(f"Touched at ({x}, {y})")

    @log_time(logger)
    def back(self) -> None:
        keyevent("BACK")
        logger.info("Pressed back button")

    @log_time(logger)
    def type(self, text: str) -> None:
        text(text)
        logger.info(f"Typed: {text}")

    @log_time(logger)
    def swipe(
        self,
        start_x: float,
        start_y: float,
        end_x: float,
        end_y: float,
        duration: float = 0.5,
    ) -> None:
        width, height = device().get_current_resolution()
        start = (int(width * start_x), int(height * start_y))
        end = (int(width * end_x), int(height * end_y))
        swipe(start, end, duration=duration)
        logger.info(f"Swiped from {start} to {end}")

    def get_resolution(self) -> Tuple[int, int]:
        return device().get_current_resolution()
