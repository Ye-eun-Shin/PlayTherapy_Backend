from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class StateTypeEntity(Base):
    __tablename__ = "tbl_state_type"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(45), nullable=False)
