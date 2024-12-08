from pydantic import BaseModel, EmailStr


class WhiteList(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True
