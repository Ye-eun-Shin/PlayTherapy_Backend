from datetime import datetime
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from core.db.common_declarative_base import Base


class ObservationEntity(Base):
    __tablename__ = "tbl_observation"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    kor_name = Column(String, nullable=False)
    eng_name = Column(String, nullable=False)
