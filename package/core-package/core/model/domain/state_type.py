from enum import IntEnum

from pydantic import BaseModel


class StateTypeEnum(IntEnum):
    READY = 1
    START = 2
    DONE = 3
    ERROR = 4
    NONE = 5

class StateType(BaseModel):
    id: StateTypeEnum
    name: str

    class Config:
        from_attributes = True
