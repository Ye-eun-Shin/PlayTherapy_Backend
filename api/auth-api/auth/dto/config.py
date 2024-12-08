from typing import List

from pydantic import BaseModel

from core.model.domain.org import Org
from core.model.domain.user import UserType


def to_camel(string: str) -> str:
    components = string.split("_")
    return components[0] + "".join(x.title() for x in components[1:])


class ConfigResponse(BaseModel):
    orgs: List[Org]
    user_types: List[UserType]

    class Config:
        alias_generator = to_camel
        populate_by_name = True
