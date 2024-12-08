from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class SigninRequest(BaseModel):
    email: str
    password: str


class SignupRequest(BaseModel):
    email: str
    name: str
    hashed_password: str
    birth_year: int
    gender: str
    highest_education_level_id: int
    years_of_experience: int
    user_type_id: int
    org_id: int


# jwt 토큰 검증을 위한 객체 정의
class AccessTokenResponse(BaseModel):
    access_token: str
