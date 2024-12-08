from typing import Optional, List
from sqlalchemy.orm import Session as SQLAlchemySession

from analyze.model.domain.observation import Observation
from analyze.model.entity.observation import ObservationEntity
from core.db.connection import ConnectionManager


class ObservationRepository:
    def __init__(self, connection_manager: ConnectionManager):
        self.connection_manager = connection_manager

    @ConnectionManager.manage_db_session
    def get(
        self, observation_id: int, db_session: Optional[SQLAlchemySession] = None
    ) -> Optional[Observation]:
        observation_entity = (
            db_session.query(ObservationEntity)
            .filter(ObservationEntity.id == observation_id)
            .first()
        )
        if observation_entity is not None:
            return Observation.model_validate(observation_entity)

        return None

    @ConnectionManager.manage_db_session
    def list(
        self,
        db_session: Optional[SQLAlchemySession] = None,
    ) -> List[Observation]:
        query = db_session.query(ObservationEntity)

        observation_entities = query.order_by(ObservationEntity.id.desc()).all()
        return (
            [Observation.model_validate(entity) for entity in observation_entities]
            if observation_entities
            else []
        )
