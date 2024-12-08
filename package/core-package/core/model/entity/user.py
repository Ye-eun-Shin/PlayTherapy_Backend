from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from core.model.entity.org import OrgEntity

Base = declarative_base()


class UserTypeEntity(Base):
    __tablename__ = "tbl_user_type"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String, nullable=False)


class HighestEducationLevelEntity(Base):
    __tablename__ = "tbl_highest_education_level"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String, nullable=False)


class UserEntity(Base):
    __tablename__ = "tbl_user"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)  # 비밀번호는 암호화해서 저장
    birth_year = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)
    highest_education_level_id = Column(
        Integer, ForeignKey("tbl_highest_education_level.id"), nullable=False
    )
    years_of_experience = Column(Integer, nullable=False)
    created_time = Column(DateTime, default=func.now())  # CURRENT_TIMESTAMP
    org_id = Column(Integer, nullable=False)
    user_type_id = Column(Integer, ForeignKey("tbl_user_type.id"), nullable=False)
