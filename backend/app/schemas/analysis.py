from pydantic import BaseModel
from typing import List, Dict, Optional


class AnalysisResult(BaseModel):
    filename: str
    name: str
    size: str
    type: str
    score: int
    risk_score: int
    summary: str
    threats: List[str]
    technical_details: Dict
    source: str
