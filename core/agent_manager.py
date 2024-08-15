import uuid
from typing import Dict, Any
from agents.base_agent import Agent
from ui_automation.ui_test_agent import UITestAgent
from utils.log import Log, log_time
from config.settings import LOG_DIR

logger = Log.log(file_name="agent_manager", dir_name=LOG_DIR)


class AgentManager:
    def __init__(self):
        self.agents: Dict[str, Agent] = {}

    @log_time(logger)
    def create_agent(self, agent_type: str, config: Dict[str, Any]) -> Agent:
        agent_id = str(uuid.uuid4())
        if agent_type == "UITestAgent":
            new_agent = UITestAgent(agent_id, config)
        else:
            new_agent = Agent(agent_id, config)
        self.agents[agent_id] = new_agent
        logger.info(f"Created new {agent_type} with ID: {agent_id}")
        return new_agent

    def get_agent(self, agent_id: str) -> Agent:
        agent = self.agents.get(agent_id)
        if agent:
            logger.info(f"Retrieved agent with ID: {agent_id}")
        else:
            logger.warning(f"Agent with ID {agent_id} not found")
        return agent

    def update_agent(self, agent_id: str, config: Dict[str, Any]) -> None:
        if agent_id in self.agents:
            self.agents[agent_id].config.update(config)
            logger.info(f"Updated agent with ID: {agent_id}")
        else:
            logger.warning(
                f"Attempted to update non-existent agent with ID: {agent_id}"
            )

    def delete_agent(self, agent_id: str) -> None:
        if self.agents.pop(agent_id, None):
            logger.info(f"Deleted agent with ID: {agent_id}")
        else:
            logger.warning(
                f"Attempted to delete non-existent agent with ID: {agent_id}"
            )
