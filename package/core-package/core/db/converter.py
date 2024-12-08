from pydantic import BaseModel
from sqlalchemy.ext.declarative import declarative_base
from typing import Type

Base = declarative_base()


def convert_to_orm(pydantic_model: BaseModel, orm_model_class: Type[Base]) -> Base:
    orm_model_instance = orm_model_class()
    for field_name, field_value in pydantic_model:
        if hasattr(orm_model_instance, field_name):
            setattr(orm_model_instance, field_name, field_value)
    return orm_model_instance

