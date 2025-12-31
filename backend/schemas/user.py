"""
User-related Pydantic schemas
"""
from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict


class UserProfileUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    portfolio_url: Optional[str] = None
    current_title: Optional[str] = None
    years_experience: Optional[int] = None
    search_keywords: Optional[str] = None
    preferences: Optional[Dict] = None
    target_companies: Optional[List[str]] = None
    blacklisted_companies: Optional[List[str]] = None
    notification_email: Optional[bool] = None
    notification_telegram: Optional[bool] = None
    telegram_chat_id: Optional[str] = None
    auto_analyze: Optional[bool] = None


class UserProfileResponse(BaseModel):
    id: int
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    portfolio_url: Optional[str] = None
    current_title: Optional[str] = None
    years_experience: Optional[int] = None
    resume_text: str
    resume_pdf_path: Optional[str] = None
    search_keywords: Optional[str] = None
    preferences: Dict = {}
    target_companies: List[str] = []
    blacklisted_companies: List[str] = []
    
    class Config:
        from_attributes = True
