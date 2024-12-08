from typing import Optional

from core.model.domain.state_type import StateType
from sqlalchemy.orm import Session

from core.model.entity.org import OrgEntity
from core.db.connection import ConnectionManager


class StateTypeRepository:
    def __init__(self, connection_manager: ConnectionManager):
        self.connection_manager = connection_manager

    @ConnectionManager.manage_db_session
    def list(self, db_session: Optional[Session] = None):
        state_type_entities = db_session.query(OrgEntity).all()
        result = []
        if state_type_entities:
            for entity in state_type_entities:
                result.append(StateType.model_validate(entity))
            return result
        return []
