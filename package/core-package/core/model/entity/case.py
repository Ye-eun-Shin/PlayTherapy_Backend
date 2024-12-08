from datetime import datetime
from sqlalchemy import Column, Integer, String, func, ForeignKey, JSON
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class CaseEntity(Base):
    __tablename__ = "tbl_case"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    given_name = Column(String, nullable=False)
    family_name = Column(String)
    description = Column(String)
    user_id = Column(Integer, nullable=False)
    start_date = Column(String)
    updated_date = Column(String)
    case_state_id = Column(Integer, nullable=False)
