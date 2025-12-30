"""
Application-related Pydantic schemas
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ApplicationCreate(BaseModel):
    job_id: int
    status: str = "saved"
    notes: Optional[str] = None


class ApplicationUpdate(BaseModel):
    status: Optional[str] = None
    applied_date: Optional[datetime] = None
    interview_date: Optional[datetime] = None
    interview_type: Optional[str] = None
    follow_up_date: Optional[datetime] = None
    notes: Optional[str] = None
    resume_version: Optional[str] = None
    cover_letter_used: Optional[str] = None
    salary_expectation: Optional[str] = None
    rejection_reason: Optional[str] = None


class ApplicationResponse(BaseModel):
    id: int
    job_id: int
    status: str
    applied_date: Optional[datetime] = None
    interview_date: Optional[datetime] = None
    interview_type: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
