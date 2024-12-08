from typing import Optional

from pydantic import BaseModel


class JwtPayload(BaseModel):
    user_id: int
    user_email: str
    user_name: str
    user_type: Optional[int] = None


class Token(BaseModel):
    access_token: str
