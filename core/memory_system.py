from typing import Dict, Any, List


class MemorySystem:
    def __init__(self):
        self.memories: Dict[str, List[Dict[str, Any]]] = {}

    def store_memory(self, agent_id: str, memory_data: Dict[str, Any]) -> None:
        if agent_id not in self.memories:
            self.memories[agent_id] = []
        self.memories[agent_id].append(memory_data)

    def retrieve_memory(
        self, agent_id: str, query: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        # 实现内存检索逻辑
        return self.memories.get(agent_id, [])
