from typing import List
from datetime import datetime
from functools import wraps
from contents.dto.session import SessionRequest
from contents.exception import (
    CaseNotFound,
    SessionNotFound,
    InvalidRange,
)
from core.model.domain.case import Case
from core.model.domain.session import Session
from core.model.domain.state_type import StateTypeEnum
from core.repository.case import CaseRepository
from core.repository.session import SessionRepository
from core.service.security import SecurityService
from core.db.connection import ConnectionManager
from core.db.transaction import transaction_scope


class SessionService:
    def __init__(
        self,
        session_repository: SessionRepository,
        case_repository: CaseRepository,
        security_service: SecurityService,
        connection_manager: ConnectionManager,
    ):
        self.session_repository = session_repository
        self.case_repository = case_repository
        self.security_service = security_service
        self.session_per_page = 10
        self.max_length = 0
        self.connection_manager = connection_manager

    def get_current_date(self):
        return datetime.now().date().strftime("%Y-%m-%d")

    def check_case_exists(func):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            case_id = kwargs.get("case_id")
            user_id = kwargs.get("user_id")
            case = self.case_repository.get(case_id=case_id, user_id=user_id)
            if not case:
                raise CaseNotFound(case_id)
            return await func(self, *args, **kwargs)

        return wrapper

    @check_case_exists
    async def add(self, case_id: int, user_id: int, data: SessionRequest) -> Session:
        db_session = self.connection_manager.make_session()
        with transaction_scope(db_session) as tx_session:
            session = data.data
            session.case_id = case_id
            session.session_state_id = StateTypeEnum.READY
            session.script_state_id = StateTypeEnum.NONE
            session.analyze_state_id = StateTypeEnum.NONE
            session.encoding_state_id = StateTypeEnum.NONE
            session.created_date = self.get_current_date()

            session = self.session_repository.add(
                session=session, db_session=tx_session
            )

        return session

    @check_case_exists
    async def get(self, case_id: int, session_id: int, user_id: int) -> Session:
        session = self.session_repository.get(session_id=session_id)
        if not session:
            raise SessionNotFound(session_id)
        return session

    @check_case_exists
    async def get_page_num(
        self, case_id: int, user_id: int, keyword: str = None
    ) -> int:
        total_sessions = self.session_repository.total_count(case_id, keyword=keyword)
        if total_sessions == 0:
            return 1
        return (total_sessions + self.session_per_page - 1) // self.session_per_page

    async def range_check(
        self, skip: int, limit: int, case_id: int, keyword: str = None
    ) -> List[Session]:
        max_length = self.session_repository.total_count(
            case_id=case_id, keyword=keyword
        )
        self.max_length = max_length
        if skip is None:
            skip = 0
        if limit is None:
            limit = max_length - skip
        if skip < 0 or limit < 0 or skip + limit > max_length:
            return False
        return True

    @check_case_exists
    async def get_session_list(
        self, case_id: int, skip: int, limit: int, user_id: int, keyword: str = None
    ) -> List[Session]:
        if not await self.range_check(skip, limit, case_id, keyword):
            if skip and limit is None:
                raise InvalidRange(skip, skip + self.max_length - 1)
            if skip is None:
                raise InvalidRange(0, limit - 1)
            raise InvalidRange(skip, skip + limit - 1)
        return self.session_repository.get_list(
            case_id=case_id, skip=skip, limit=limit, keyword=keyword
        )

    @check_case_exists
    async def update(
        self, case_id: int, session_id: int, user_id: int, data: SessionRequest
    ) -> Session:
        db_session = self.connection_manager.make_session()
        with transaction_scope(db_session) as tx_session:
            session = data.data
            res = self.session_repository.update(
                session_id=session_id,
                session=session,
                db_session=tx_session,
            )
            if not res:
                raise SessionNotFound(session_id)

        return session

    @check_case_exists
    async def delete(self, case_id: int, session_id: int, user_id: int) -> bool:
        db_session = self.connection_manager.make_session()
        with transaction_scope(db_session) as tx_session:
            res = self.session_repository.delete(
                session_id=session_id, db_session=tx_session
            )
            if not res:
                raise SessionNotFound(session_id)

        return True
