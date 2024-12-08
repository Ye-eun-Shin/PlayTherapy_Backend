from typing import List, Any, Dict
from pydantic import BaseModel, Field


class BatchPromptReport(BaseModel):
    category: str = Field(default="unknown")
    descriptions: str = Field(default="")
    interactions: list = Field(default_factory=list)
    level: int = Field(default=-1)


class AnalyzeReport(BaseModel):
    reports: Dict[str, BatchPromptReport] = {}
