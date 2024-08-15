from typing import Dict, Any, List, Callable


class CommunicationHub:
    def __init__(self):
        self.subscribers: Dict[str, List[Callable]] = {}

    def publish(self, topic: str, message: Any) -> None:
        if topic in self.subscribers:
            for callback in self.subscribers[topic]:
                callback(message)

    def subscribe(self, topic: str, callback: Callable) -> None:
        if topic not in self.subscribers:
            self.subscribers[topic] = []
        self.subscribers[topic].append(callback)
