from typing import List


class MonitoringService:
    def __init__(self):
        self.logs: List[str] = []

    def log_event(self, event: str) -> None:
        self.logs.append(event)

    def get_logs(self) -> List[str]:
        return self.logs
