from datetime import datetime
from typing_extensions import Annotated
from typing import Optional
from pydantic import BaseModel, EmailStr, StringConstraints


class User(BaseModel):
    id: Optional[int]
    email: EmailStr
    name: Annotated[str, StringConstraints(min_length=1)]
    hashed_password: Annotated[str, StringConstraints(min_length=1)]
    birth_year: int
    gender: str
    highest_education_level_id: int
    years_of_experience: int
    created_time: Optional[datetime]
    user_type_id: int
    org_id: int

    class Config:
        from_attributes = True


class UserType(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
