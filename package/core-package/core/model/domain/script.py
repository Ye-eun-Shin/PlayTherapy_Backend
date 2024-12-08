from datetime import datetime
from typing import List
from pydantic import BaseModel, Field


def get_current_time():
    return datetime.now().time().strftime("%H:%M:%S.%f")


class Record(BaseModel):
    speaker: str = Field("Unknown")
    text: str = Field("Unknown")
    start_time: str = Field(default_factory=get_current_time)
    end_time: str = Field(default_factory=get_current_time)


class Script(BaseModel):
    scripts: List[Record] = Field(default_factory=list)
