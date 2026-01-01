"""
Manual Preparation Model
Stores manually created interview preparation sessions
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Index
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
from database import Base


class ManualPrep(Base):
    """Manual interview preparation sessions"""
    __tablename__ = "manual_preps"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user_profile.id'), default=1)
    
    # Manual input fields
    job_url = Column(String)  # Job posting URL
    company_name = Column(String, nullable=False, index=True)
    job_title = Column(String)
    job_description = Column(Text)
    
    # AI-generated content (using DeepSeek models)
    company_insights = Column(Text)  # JSON: Company info, culture, recent news
    technical_qa = Column(Text)  # JSON: Technical questions with answers
    behavioral_qa = Column(Text)  # JSON: Behavioral questions with STAR examples
    hr_qa = Column(Text)  # JSON: HR/salary questions with answers
    key_talking_points = Column(Text)  # JSON: Important points to emphasize
    preparation_tips = Column(Text)  # JSON: Specific tips for this company/role
    
    # Metadata
    created_at = Column(DateTime, default=datetime.now, index=True)
    expires_at = Column(DateTime, default=lambda: datetime.now() + timedelta(days=30))
    is_favorite = Column(Boolean, default=False)
    notes = Column(Text)  # User's personal notes
    
    # Status tracking
    status = Column(String, default='active')  # active, archived, completed
    interview_date = Column(DateTime)
    
    # User relationship
    user = relationship("UserProfile", back_populates="manual_preps")
    
    def to_dict(self):
        """Convert to dictionary"""
        import json
        
        def safe_json_parse(text, default=None):
            if not text:
                return default
            try:
                return json.loads(text)
            except:
                return default
        
        return {
            "id": self.id,
            "user_id": self.user_id,
            "job_url": self.job_url,
            "company_name": self.company_name,
            "job_title": self.job_title,
            "job_description": self.job_description,
            "company_insights": safe_json_parse(self.company_insights, {}),
            "technical_qa": safe_json_parse(self.technical_qa, []),
            "behavioral_qa": safe_json_parse(self.behavioral_qa, []),
            "hr_qa": safe_json_parse(self.hr_qa, []),
            "key_talking_points": safe_json_parse(self.key_talking_points, []),
            "preparation_tips": safe_json_parse(self.preparation_tips, []),
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "is_favorite": self.is_favorite,
            "notes": self.notes,
            "status": self.status,
            "interview_date": self.interview_date.isoformat() if self.interview_date else None,
            "days_remaining": (self.expires_at - datetime.now()).days if self.expires_at else None
        }
    
    def __repr__(self):
        return f"<ManualPrep(id={self.id}, company='{self.company_name}', title='{self.job_title}')>"


# Indexes for performance
Index('idx_manual_prep_company', ManualPrep.company_name)
Index('idx_manual_prep_status', ManualPrep.status)
Index('idx_manual_prep_expires', ManualPrep.expires_at)
Index('idx_manual_prep_created', ManualPrep.created_at)
