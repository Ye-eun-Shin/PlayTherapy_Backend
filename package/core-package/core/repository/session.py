from typing import Optional, List
from sqlalchemy.orm import Session as SQLAlchemySession

from core.model.domain.session import Session as SessionDomain
from core.model.domain.state_type import StateTypeEnum
from core.model.entity.session import SessionEntity
from core.db.connection import ConnectionManager

from sqlalchemy.exc import OperationalError


class SessionRepository:
    def __init__(self, connection_manager: ConnectionManager):
        self.connection_manager = connection_manager

    @ConnectionManager.manage_db_session_with_transaction
    def add(
        self, session: SessionDomain, db_session: Optional[SQLAlchemySession] = None
    ) -> SessionDomain:
        session_entity = SessionEntity(**session.model_dump())
        db_session.add(session_entity)
        db_session.flush()

        return SessionDomain.model_validate(session_entity)

    @ConnectionManager.manage_db_session
    def get(
        self, session_id: int, db_session: Optional[SQLAlchemySession] = None
    ) -> Optional[SessionDomain]:
        session_entity = (
            db_session.query(SessionEntity)
            .filter(SessionEntity.id == session_id)
            .first()
        )
        if session_entity is not None:
            return SessionDomain.model_validate(session_entity)

        return None

    @ConnectionManager.manage_db_session
    def total_count(
        self,
        case_id: int,
        keyword: str = None,
        db_session: Optional[SQLAlchemySession] = None,
    ) -> int:
        query = db_session.query(SessionEntity).filter(SessionEntity.case_id == case_id)
        if keyword:
            query = query.filter(SessionEntity.name.like(f"%{keyword}%"))
        total_sessions = query.count()
        return total_sessions

    @ConnectionManager.manage_db_session
    def get_list(
        self,
        case_id: int = None,
        skip: int = None,
        limit: int = None,
        keyword: str = None,
        db_session: Optional[SQLAlchemySession] = None,
    ) -> List[SessionDomain]:
        query = db_session.query(SessionEntity)
        if case_id:
            query = query.filter(SessionEntity.case_id == case_id)
        if keyword:
            query = query.filter(SessionEntity.name.like(f"%{keyword}%"))

        session_entities = (
            query.order_by(SessionEntity.id.desc()).offset(skip).limit(limit).all()
        )
        return (
            [SessionDomain.model_validate(entity) for entity in session_entities]
            if session_entities
            else []
        )

    @ConnectionManager.manage_db_session
    def list_by_state_id(
        self, state_id: StateTypeEnum, db_session: Optional[SQLAlchemySession] = None
    ) -> (List)[SessionDomain]:
        session_entities = (
            db_session.query(SessionEntity)
            .filter(SessionEntity.session_state_id == int(state_id))
            .all()
        )

        return (
            [SessionDomain.model_validate(entity) for entity in session_entities]
            if session_entities
            else []
        )

    @ConnectionManager.manage_db_session_with_transaction
    def get_by_script_state_id(
        self, state_id: StateTypeEnum, db_session: Optional[SQLAlchemySession] = None
    ) -> Optional[SessionDomain]:
        session_entity = (
            db_session.query(SessionEntity)
            .filter(SessionEntity.script_state_id == int(state_id))
            .first()
        )
        if session_entity is None:
            return None

        return SessionDomain.model_validate(session_entity)

    @ConnectionManager.manage_db_session_with_transaction
    def get_by_analyze_state_id(
        self, state_id: StateTypeEnum, db_session: Optional[SQLAlchemySession] = None
    ) -> Optional[SessionDomain]:
        session_entity = (
            db_session.query(SessionEntity)
            .filter(SessionEntity.analyze_state_id == int(state_id))
            .first()
        )
        if session_entity is None:
            return None

        return SessionDomain.model_validate(session_entity)

    @ConnectionManager.manage_db_session_with_transaction
    def get_by_encode_state_id(
        self, state_id: StateTypeEnum, db_session: Optional[SQLAlchemySession] = None
    ) -> Optional[SessionDomain]:
        session_entity = (
            db_session.query(SessionEntity)
            .filter(SessionEntity.encoding_state_id == int(state_id))
            .first()
        )

        if session_entity is None:
            return None

        return SessionDomain.model_validate(session_entity)

    @ConnectionManager.manage_db_session_with_transaction
    def update_state_by_session_id(
        self,
        session_id: int,
        new_state_id: StateTypeEnum,
        db_session: Optional[SQLAlchemySession] = None,
    ) -> bool:
        update_count = (
            db_session.query(SessionEntity)
            .filter(SessionEntity.id == session_id)
            .update({"session_state_id": int(new_state_id)})
        )

        return update_count > 0

    @ConnectionManager.manage_db_session_with_transaction
    def update_script_state_by_session_id(
        self,
        session_id: int,
        new_state_id: StateTypeEnum,
        db_session: Optional[SQLAlchemySession] = None,
    ) -> bool:
        update_count = (
            db_session.query(SessionEntity)
            .filter(SessionEntity.id == session_id)
            .update({"script_state_id": int(new_state_id)})
        )

        return update_count > 0

    @ConnectionManager.manage_db_session_with_transaction
    def update_analyze_state_by_session_id(
        self,
        session_id: int,
        new_state_id: StateTypeEnum,
        db_session: Optional[SQLAlchemySession] = None,
    ) -> bool:
        update_count = (
            db_session.query(SessionEntity)
            .filter(SessionEntity.id == session_id)
            .update({"analyze_state_id": int(new_state_id)})
        )

        return update_count > 0

    @ConnectionManager.manage_db_session_with_transaction
    def update(
        self,
        session_id: int,
        session: SessionDomain,
        db_session: Optional[SQLAlchemySession] = None,
    ):
        update_count = (
            db_session.query(SessionEntity)
            .filter(SessionEntity.id == session_id)
            .update(session.model_dump())
        )

        return update_count > 0

    @ConnectionManager.manage_db_session_with_transaction
    def delete(
        self, session_id: int, db_session: Optional[SQLAlchemySession] = None
    ) -> bool:
        delete_count = (
            db_session.query(SessionEntity)
            .filter(SessionEntity.id == session_id)
            .delete()
        )
        return delete_count > 0

    @ConnectionManager.manage_db_session_with_transaction
    def update_url(
        self,
        session_id: int,
        url_type: str,
        url: str,
        db_session: Optional[SQLAlchemySession] = None,
    ) -> bool:
        update_count = (
            db_session.query(SessionEntity)
            .filter(SessionEntity.id == session_id)
            .update(
                {
                    url_type: url,
                }
            )
        )
        return update_count > 0
