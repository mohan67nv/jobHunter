"""
Job-related Pydantic schemas
"""
from pydantic import BaseModel, HttpUrl
from typing import Optional, List
from datetime import datetime


class JobBase(BaseModel):
    title: str
    company: str
    location: str
    description: str
    url: str
    source: str
    salary: Optional[str] = None
    job_type: Optional[str] = None
    contract_type: Optional[str] = None
    remote_type: Optional[str] = None
    experience_level: Optional[str] = None


class JobCreate(JobBase):
    posted_date: datetime
    requirements: Optional[str] = None
    benefits: Optional[str] = None


class JobUpdate(BaseModel):
    is_active: Optional[bool] = None
    view_count: Optional[int] = None


class JobResponse(JobBase):
    id: int
    posted_date: datetime
    scraped_date: datetime
    is_active: bool
    is_duplicate: bool
    duplicate_of: Optional[int] = None
    view_count: int
    created_at: datetime
    updated_at: datetime
    match_score: Optional[float] = None  # Match score from JobAnalysis
    ats_score: Optional[float] = None    # ATS score from JobAnalysis
    
    class Config:
        from_attributes = True


class JobListResponse(BaseModel):
    jobs: List[JobResponse]
    total: int
    page: int
    page_size: int
