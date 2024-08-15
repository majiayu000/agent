import threading
import time
from typing import List, Any
from config.settings import USE_HEALTH_CHECK, HEALTH_CHECK_CONFIG


class HealthCheck:
    def __init__(self, components: List[Any]):
        self.components = components
        self.config = HEALTH_CHECK_CONFIG
        if USE_HEALTH_CHECK:
            self.thread = threading.Thread(target=self.run_health_check)
            self.thread.daemon = True
            self.thread.start()

    def run_health_check(self) -> None:
        while True:
            for component in self.components:
                try:
                    component.health_check()
                except Exception as e:
                    print(
                        f"Health check failed for {component.__class__.__name__}: {str(e)}"
                    )
                    self.recover_component(component)
            time.sleep(self.config["interval"])

    def recover_component(self, component: Any) -> None:
        try:
            component.recover()
        except Exception as e:
            print(f"Recovery failed for {component.__class__.__name__}: {str(e)}")
