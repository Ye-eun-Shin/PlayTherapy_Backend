from typing import Optional
from sqlalchemy.orm import Session

from core.model.domain.org import Org
from core.model.entity.org import OrgEntity
from core.db.connection import ConnectionManager


class OrgRepository:
    def __init__(self, connection_manager: ConnectionManager):
        self.connection_manager = connection_manager

    @ConnectionManager.manage_db_session
    def get(self, org_id: int, db_session: Optional[Session] = None) -> Optional[Org]:
        org_entity = db_session.query(OrgEntity).filter(OrgEntity.id == org_id).first()
        if org_entity is not None:
            return Org.model_validate(org_entity)

        return None

    @ConnectionManager.manage_db_session
    def list(self, db_session: Optional[Session] = None):
        org_entities = db_session.query(OrgEntity).all()
        result = []
        if org_entities:
            for entity in org_entities:
                result.append(Org.model_validate(entity))
            return result
        return []
