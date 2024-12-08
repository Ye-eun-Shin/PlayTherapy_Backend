from typing import Optional, List
from sqlalchemy.orm import Session

from core.model.domain.user import User, UserType
from core.model.entity.user import UserEntity, UserTypeEntity
from core.db.connection import ConnectionManager


class UserRepository:
    def __init__(self, connection_manager: ConnectionManager):
        self.connection_manager = connection_manager

    @ConnectionManager.manage_db_session_with_transaction
    def add(self, user: User, db_session: Optional[Session] = None):
        user_entity = UserEntity(**user.model_dump())
        db_session.add(user_entity)
        db_session.flush()
        
        return User.model_validate(user_entity)

    @ConnectionManager.manage_db_session
    def get_by_id(
        self, user_id: int, db_session: Optional[Session] = None
    ) -> Optional[User]:
        user_entity = (
            db_session.query(UserEntity).filter(UserEntity.id == user_id).first()
        )
        if user_entity:
            return User.model_validate(user_entity)
        return None

    @ConnectionManager.manage_db_session
    def get_by_email(
        self, email: str, db_session: Optional[Session] = None
    ) -> Optional[User]:
        user_entity = (
            db_session.query(UserEntity).filter(UserEntity.email == email).first()
        )
        if user_entity:
            return User.model_validate(user_entity)
        return None

    @ConnectionManager.manage_db_session
    def get_by_email_and_password(
        self, email: str, hashed_password: str, db_session: Optional[Session] = None
    ) -> Optional[User]:
        user_entity = (
            db_session.query(UserEntity)
            .filter(UserEntity.email == email)
            .filter(UserEntity.hashed_password == hashed_password)
            .first()
        )
        if user_entity:
            return User.model_validate(user_entity)
        return None


class UserTypeRepository:
    def __init__(self, connection_manager: ConnectionManager):
        self.connection_manager = connection_manager

    @ConnectionManager.manage_db_session
    def list(self, db_session: Optional[Session] = None) -> List[UserType]:
        user_type_entities = db_session.query(UserTypeEntity).all()
        result = []
        if user_type_entities:
            for entity in user_type_entities:
                result.append(UserType.model_validate(entity))
            return result
        return []
