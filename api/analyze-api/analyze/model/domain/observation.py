from pydantic import BaseModel


class Observation(BaseModel):
    id: int
    kor_name: str = "Unknown"
    eng_name: str = "Unknown"

    class Config:
        from_attributes = True
