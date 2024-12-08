from typing import Optional, List
from functools import wraps
from sqlalchemy import or_, and_, func
from sqlalchemy.orm import Session

from core.model.domain.case import Case
from core.model.entity.case import CaseEntity
from core.model.entity.session import SessionEntity
from core.db.connection import ConnectionManager


class CaseRepository:
    def __init__(self, connection_manager: ConnectionManager):
        self.connection_manager = connection_manager

    @ConnectionManager.manage_db_session_with_transaction
    def add(self, case: Case, db_session: Optional[Session] = None) -> Case:
        case_entity = CaseEntity(**case.model_dump(exclude={"session_count"}))
        db_session.add(case_entity)
        return case

    @ConnectionManager.manage_db_session
    def get(
        self, case_id: int, user_id: int = None, db_session: Optional[Session] = None
    ) -> Case:
        query = (
            db_session.query(
                CaseEntity,
                func.count(SessionEntity.case_id).label("session_count"),
            )
            .join(SessionEntity, CaseEntity.id == SessionEntity.case_id, isouter=True)
            .filter(CaseEntity.id == case_id)
            .group_by(CaseEntity.id)
        )

        if user_id:
            query = query.filter(CaseEntity.user_id == user_id)

        result = query.first()
        if result:
            case_entity, session_count = result
            return Case.model_validate(case_entity, session_count)

        return None

    @ConnectionManager.manage_db_session
    def total_count(
        self,
        user_id: int = None,
        keyword: str = None,
        db_session: Optional[Session] = None,
    ) -> int:
        query = db_session.query(CaseEntity)
        if user_id:
            query = query.filter(CaseEntity.user_id == user_id)
        if keyword:
            query = query.filter(
                or_(
                    CaseEntity.name.like(f"%{keyword}%"),
                    CaseEntity.description.like(f"%{keyword}%"),
                )
            )
        total_cases = query.count()
        return total_cases

    # TODO: description 속 key 문자열("age","gender") 삭제 후 키워드 검색
    @ConnectionManager.manage_db_session
    def get_list(
        self,
        user_id: int = None,
        skip: int = None,
        limit: int = None,
        keyword: str = None,
        db_session: Optional[Session] = None,
    ) -> List[Case]:
        query = (
            db_session.query(
                CaseEntity,
                func.count(SessionEntity.case_id).label("session_count"),
            )
            .join(SessionEntity, CaseEntity.id == SessionEntity.case_id, isouter=True)
            .group_by(CaseEntity.id)
        )
        if user_id:
            query = query.filter(CaseEntity.user_id == user_id)
        if keyword:
            query = query.filter(
                or_(
                    CaseEntity.name.like(f"%{keyword}%"),
                    func.replace(
                        func.replace(CaseEntity.description, "age", ""), "gender", ""
                    ).like(f"%{keyword}%"),
                )
            )
        case_entities = (
            query.order_by(CaseEntity.id.desc()).offset(skip).limit(limit).all()
        )

        result = []
        for case_entity, session_count in case_entities:
            result.append(Case.model_validate(case_entity, session_count))
        return result

    @ConnectionManager.manage_db_session_with_transaction
    def update(
        self,
        case_id: int,
        user_id: int,
        case: Case,
        db_session: Optional[Session] = None,
    ) -> Case:
        update_count = (
            db_session.query(CaseEntity)
            .filter(and_(CaseEntity.user_id == user_id, CaseEntity.id == case_id))
            .update(case.model_dump(exclude={"session_count"}))
        )

        return update_count > 0

    @ConnectionManager.manage_db_session_with_transaction
    def delete(self, case_id: int, user_id: int, db_session: Optional[Session] = None):
        delete_count = (
            db_session.query(CaseEntity)
            .filter(and_(CaseEntity.user_id == user_id, CaseEntity.id == case_id))
            .delete()
        )
        return delete_count > 0
