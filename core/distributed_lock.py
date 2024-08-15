import redis
from typing import Optional
from config.settings import USE_DISTRIBUTED_LOCK, DISTRIBUTED_LOCK_CONFIG
from redis.lock import Lock  # 添加这行导入


class DistributedLock:
    def __init__(self):
        if USE_DISTRIBUTED_LOCK:
            self.redis_client = redis.Redis(**DISTRIBUTED_LOCK_CONFIG)
        else:
            self.redis_client = None

    def acquire_lock(
        self, lock_name: str, timeout: int = 10
    ) -> Optional[Lock]:  # 修改这里
        if USE_DISTRIBUTED_LOCK:
            return self.redis_client.lock(lock_name, timeout=timeout)
        return None

    def release_lock(self, lock: Optional[Lock]) -> None:  # 修改这里
        if USE_DISTRIBUTED_LOCK and lock:
            lock.release()
