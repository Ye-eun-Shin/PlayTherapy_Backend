from sqlalchemy import Column, ForeignKey, BigInteger, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class SessionEntity(Base):
    __tablename__ = "tbl_session"

    id = Column(BigInteger, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(128))
    session_state_id = Column(Integer, nullable=False)
    case_id = Column(BigInteger, nullable=False)
    source_video_url = Column(String(1024))
    source_script_url = Column(String(1024))
    encoding_state_id = Column(Integer, nullable=False, default=0)
    script_state_id = Column(Integer, nullable=False, default=0)
    analyze_state_id = Column(Integer, nullable=False, default=0)
    created_date = Column(String(128))
    video_length = Column(String(128))
    origin_video_url = Column(String(1024))
    encoding_video_url = Column(String(1024))
    analyze_url = Column(String(1024))
