from typing import List
import json
from datetime import datetime
from contents.dto.case import CaseRequest
from contents.exception import (
    CaseNotFound,
    InvalidRange,
)
from core.model.domain.case import Case
from core.model.domain.state_type import StateTypeEnum
from core.repository.case import CaseRepository
from core.service.security import SecurityService
from core.db.connection import ConnectionManager
from core.db.transaction import transaction_scope


class CaseService:
    def __init__(
        self,
        case_repository: CaseRepository,
        security_service: SecurityService,
        connection_manager: ConnectionManager,
    ):
        self.case_repository = case_repository
        self.security_service = security_service
        self.case_per_page = 10
        self.max_length = 0
        self.connection_manager = connection_manager

    def get_current_date(self):
        return datetime.now().date().strftime("%Y-%m-%d")

    async def add(self, user_id: int, data: CaseRequest) -> Case:
        db_session = self.connection_manager.make_session()
        with transaction_scope(db_session) as tx_session:
            case = Case(
                description=json.dumps(data.description),
                user_id=user_id,
                start_date=self.get_current_date(),
                updated_date=self.get_current_date(),
                case_state_id=StateTypeEnum.READY,
                **data.model_dump(
                    exclude={
                        "description",
                        "user_id",
                        "start_date",
                        "updated_date",
                        "case_state_id",
                    }
                )
            )
            added_case = self.case_repository.add(case=case, db_session=tx_session)

        return added_case

    # TODO: Resolving Case description pydantic warning
    async def get(self, case_id: int, user_id: int = None) -> Case:
        case = self.case_repository.get(case_id=case_id, user_id=user_id)
        if not case:
            raise CaseNotFound(case_id)
        case.description = json.loads(case.description)
        return case

    async def get_page_num(self, user_id: int = None, keyword: str = None) -> int:
        total_cases = self.case_repository.total_count(user_id, keyword=keyword)
        if total_cases == 0:
            return 1
        return (total_cases + self.case_per_page - 1) // self.case_per_page

    async def range_check(
        self, skip: int, limit: int, user_id: int = None, keyword: str = None
    ) -> bool:
        max_length = self.case_repository.total_count(user_id=user_id, keyword=keyword)
        self.max_length = max_length
        if skip is None:
            skip = 0
        if limit is None:
            limit = max_length - skip
        if skip < 0 or limit < 0 or skip + limit > max_length:
            return False
        return True

    # TODO: Resolving Case description pydantic warning
    async def get_case_list(
        self, skip: int, limit: int, user_id: int = None, keyword: str = None
    ) -> List[Case]:
        if not await self.range_check(skip, limit, user_id, keyword):
            if skip and limit is None:
                raise InvalidRange(skip, skip + self.max_length - 1)
            if skip is None:
                raise InvalidRange(0, limit - 1)
            raise InvalidRange(skip, skip + limit - 1)

        case_list = self.case_repository.get_list(user_id, skip, limit, keyword)
        for case in case_list:
            case.description = json.loads(case.description)
        return case_list

    async def update(self, user_id: int, case_id: int, case: CaseRequest) -> Case:
        db_session = self.connection_manager.make_session()
        with transaction_scope(db_session) as tx_session:
            case.updated_date = self.get_current_date()
            if case.description:
                case = Case(
                    description=json.dumps(case.description),
                    **case.model_dump(exclude={"description"})
                )
            else:
                case = Case(**case.model_dump())

            result = self.case_repository.update(
                case_id, user_id, case=case, db_session=tx_session
            )
            if not result:
                raise CaseNotFound(case_id)
        return case

    async def delete(self, user_id: int, case_id: int) -> bool:
        db_session = self.connection_manager.make_session()
        with transaction_scope(db_session) as tx_session:
            res = self.case_repository.delete(
                case_id=case_id, user_id=user_id, db_session=tx_session
            )
            if not res:
                raise CaseNotFound(case_id)
        return True
