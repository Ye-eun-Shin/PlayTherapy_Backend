from typing import Optional

from core.model.domain.user import User
from sqlalchemy.orm import Session

from core.model.domain.whitelist import WhiteList
from core.model.entity.whitelist import WhiteListEntity
from core.db.connection import ConnectionManager


class WhitelistRepository:
    def __init__(self, connection_manager: ConnectionManager):
        self.connection_manager = connection_manager

    @ConnectionManager.manage_db_session
    def get(
        self, email: str, db_session: Optional[Session] = None
    ) -> Optional[WhiteList]:
        whitelist = (
            db_session.query(WhiteListEntity)
            .filter(WhiteListEntity.email == email)
            .first()
        )
        if whitelist is not None:
            return WhiteList.model_validate(whitelist)

        return None
