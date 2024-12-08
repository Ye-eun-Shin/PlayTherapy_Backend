from pydantic import BaseModel, StringConstraints
from typing_extensions import Annotated


class Org(BaseModel):
    id: int
    name: Annotated[str, StringConstraints(min_length=1)]

    class Config:
        from_attributes = True
