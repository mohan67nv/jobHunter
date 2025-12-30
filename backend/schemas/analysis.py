"""
Analysis-related Pydantic schemas
"""
from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime


class AnalysisRequest(BaseModel):
    job_id: int
    generate_materials: bool = True


class AnalysisResponse(BaseModel):
    id: int
    job_id: int
    match_score: Optional[float] = None
    ats_score: Optional[float] = None
    matching_skills: List[str] = []
    missing_skills: List[str] = []
    experience_match: Optional[str] = None
    salary_match: Optional[str] = None
    keyword_density: Optional[float] = None
    recommendations: Dict = {}
    tailored_resume: Optional[str] = None
    tailored_cover_letter: Optional[str] = None
    interview_questions: List[str] = []
    analyzed_at: datetime
    
    class Config:
        from_attributes = True
