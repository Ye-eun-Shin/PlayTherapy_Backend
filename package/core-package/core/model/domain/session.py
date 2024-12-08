from pydantic import BaseModel
from typing import Optional


class Session(BaseModel):
    id: Optional[int]
    name: Optional[str]
    session_state_id: Optional[int]
    case_id: Optional[int]
    source_video_url: Optional[str] = None
    source_script_url: Optional[str] = None
    encoding_state_id: Optional[int] = None
    script_state_id: Optional[int]
    analyze_state_id: Optional[int]
    created_date: Optional[str]
    video_length: Optional[str] = None
    origin_video_url: Optional[str] = None
    encoding_video_url: Optional[str] = None
    analyze_url: Optional[str] = None

    class Config:
        from_attributes = True
