from pydantic import BaseModel
from typing import Optional
from core.model.entity.case import CaseEntity


class Case(BaseModel):
    id: Optional[int]
    given_name: str
    family_name: Optional[str]
    description: Optional[str]
    user_id: int
    session_count: Optional[int] = 0
    start_date: Optional[str]
    updated_date: Optional[str]
    case_state_id: int = 1  # start

    class Config:
        from_attributes = True

    @classmethod
    def model_validate(cls, case_entity: CaseEntity, session_count: int) -> "Case":
        case = cls(**case_entity.__dict__)
        case.session_count = session_count
        return case
