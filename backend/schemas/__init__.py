"""
Pydantic schemas for API request/response validation
"""
from schemas.job import JobCreate, JobUpdate, JobResponse, JobListResponse
from schemas.analysis import AnalysisResponse, AnalysisRequest
from schemas.user import UserProfileUpdate, UserProfileResponse
from schemas.application import ApplicationCreate, ApplicationUpdate, ApplicationResponse

__all__ = [
    "JobCreate",
    "JobUpdate",
    "JobResponse",
    "JobListResponse",
    "AnalysisResponse",
    "AnalysisRequest",
    "UserProfileUpdate",
    "UserProfileResponse",
    "ApplicationCreate",
    "ApplicationUpdate",
    "ApplicationResponse",
]
