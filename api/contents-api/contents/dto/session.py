from pydantic import BaseModel, Json
from typing import Optional, Any
from core.model.domain.session import Session


class SessionRequest(BaseModel):
    data: Session
