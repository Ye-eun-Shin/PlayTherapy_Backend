from pydantic import BaseModel
from typing import Any, Dict, Optional


class CaseRequest(BaseModel):
    id: Optional[int]
    given_name: str
    family_name: Optional[str]
    description: Optional[Dict[str, Any]]
    user_id: Optional[int]
    start_date: Optional[str]
    updated_date: Optional[str]
    case_state_id: Optional[int] = 1
