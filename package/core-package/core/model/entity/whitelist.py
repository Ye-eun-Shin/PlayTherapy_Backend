from sqlalchemy import (
    Column, String, Integer
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class WhiteListEntity(Base):
    __tablename__ = 'tbl_whitelist'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    email = Column(String, nullable=False)