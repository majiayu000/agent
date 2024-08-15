from sqlalchemy import create_engine, Column, String, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Dict, Any, Optional
from config.settings import USE_DATA_PERSISTENCE, DATABASE_CONFIG

Base = declarative_base()


class AgentData(Base):
    __tablename__ = "agents"

    id = Column(String, primary_key=True)
    type = Column(String)
    config = Column(JSON)


class DataPersistence:
    def __init__(self):
        if USE_DATA_PERSISTENCE:
            self.engine = create_engine(
                DATABASE_CONFIG["url"],
                **{k: v for k, v in DATABASE_CONFIG.items() if k != "url"}
            )
            Base.metadata.create_all(self.engine)
            self.Session = sessionmaker(bind=self.engine)
        else:
            self.engine = None
            self.Session = None

    def save_agent(
        self, agent_id: str, agent_type: str, config: Dict[str, Any]
    ) -> None:
        if USE_DATA_PERSISTENCE:
            session = self.Session()
            agent_data = AgentData(id=agent_id, type=agent_type, config=config)
            session.add(agent_data)
            session.commit()
            session.close()

    def load_agent(self, agent_id: str) -> Optional[AgentData]:
        if USE_DATA_PERSISTENCE:
            session = self.Session()
            agent_data = session.query(AgentData).filter_by(id=agent_id).first()
            session.close()
            return agent_data
        return None
