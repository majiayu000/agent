import logging
import os
import time
from datetime import datetime, timedelta
from functools import wraps
from logging.handlers import TimedRotatingFileHandler
from typing import Any, Callable, TypeVar, Optional
from rich.logging import RichHandler


F = TypeVar("F", bound=Callable[..., Any])


class Log:
    log_name: str = ""
    dir_name: str = "log"
    log_names: list[str] = []
    dir_names: list[str] = []
    file_names: list[str] = []

    @classmethod
    def log(
        cls, file_name: Optional[str] = None, dir_name: Optional[str] = None
    ) -> logging.Logger:
        log_name, dir_name, file_name = cls._prepare_log_params(file_name, dir_name)

        if cls._logger_exists(log_name, dir_name, file_name):
            return logging.getLogger(log_name)

        cls._update_log_records(log_name, dir_name, file_name)
        return cls._create_logger(log_name, dir_name, file_name)

    @classmethod
    def _prepare_log_params(
        cls, file_name: Optional[str], dir_name: Optional[str]
    ) -> tuple[str, str, str]:
        if not cls.log_name:
            cls.log_name = "root"
            log_name = cls.log_name
            cls.dir_name = f"{cls.dir_name}/{dir_name}" if dir_name else cls.dir_name
            dir_name = cls.dir_name
            file_name = file_name or cls.log_name
        else:
            dir_name = f"{cls.dir_name}/{dir_name}" if dir_name else cls.dir_name
            log_name = file_name or cls.log_name
            file_name = file_name or log_name
        return log_name, dir_name, file_name

    @classmethod
    def _logger_exists(cls, log_name: str, dir_name: str, file_name: str) -> bool:
        return all(
            [
                log_name in cls.log_names,
                dir_name in cls.dir_names,
                file_name in cls.file_names,
            ]
        )

    @classmethod
    def _update_log_records(cls, log_name: str, dir_name: str, file_name: str) -> None:
        if log_name not in cls.log_names:
            cls.log_names.append(log_name)
        if dir_name not in cls.dir_names:
            cls.dir_names.append(dir_name)
        if file_name not in cls.file_names:
            cls.file_names.append(file_name)

    @staticmethod
    def _create_logger(log_name: str, dir_name: str, file_name: str) -> logging.Logger:
        def localtime(*args) -> time.struct_time:
            return (datetime.utcnow() + timedelta(hours=8)).timetuple()

        root_path = os.path.split(os.path.abspath(os.path.dirname(__file__)))[0]
        dir_path = f"{root_path}/{dir_name}"
        os.makedirs(dir_path, exist_ok=True)

        service_name = "incredible"
        fmt = f"%(asctime)s | {service_name} |  %(levelname)s  | %(filename)s | %(lineno)d |  %(funcName)s |  %(message)s"

        logging.Formatter.converter = localtime
        logging.basicConfig(level=logging.INFO, format=fmt)
        formatter = logging.Formatter(fmt)

        file_handler = TimedRotatingFileHandler(
            f"{dir_path}/{file_name}",
            when="D",
            interval=1,
            backupCount=30,
            encoding="utf-8",
        )
        file_handler.setFormatter(formatter)

        logger = logging.getLogger(None if log_name == "root" else log_name)
        logger.addHandler(file_handler)
        logger.addHandler(RichHandler())
        logger.propagate = False

        return logger


def log_time(logger: logging.Logger) -> Callable[[F], F]:
    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            start_time = time.time()
            result = func(*args, **kwargs)
            elapsed_time = (time.time() - start_time) * 1000
            logger.info(f"{func.__name__} 执行时间: {elapsed_time:.2f} ms")
            return result

        return wrapper

    return decorator
