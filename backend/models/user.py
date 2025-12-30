"""
User profile, resume versions, and cover letter templates
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, CheckConstraint
from sqlalchemy.sql import func
from database import Base


class UserProfile(Base):
    """User profile model - singleton table (only one row)"""
    __tablename__ = "user_profile"
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    linkedin_url = Column(String)
    github_url = Column(String)
    portfolio_url = Column(String)
    current_title = Column(String)
    years_experience = Column(Integer)
    resume_text = Column(Text, nullable=False)  # Extracted text from PDF/DOCX
    resume_pdf_path = Column(String)
    resume_docx_path = Column(String)
    preferences = Column(Text)  # JSON: {keywords: [...], locations: [...], salary_min: 60000}
    target_companies = Column(Text)  # JSON array of company names
    blacklisted_companies = Column(Text)  # JSON array to exclude
    notification_email = Column(Boolean, default=True)
    notification_telegram = Column(Boolean, default=False)
    telegram_chat_id = Column(String)
    auto_analyze = Column(Boolean, default=True)  # Auto-run AI analysis on new jobs
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    __table_args__ = (
        CheckConstraint('id = 1', name='singleton_user_profile'),
    )
    
    def __repr__(self):
        return f"<UserProfile(name='{self.name}', email='{self.email}')>"
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        import json
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "linkedin_url": self.linkedin_url,
            "github_url": self.github_url,
            "portfolio_url": self.portfolio_url,
            "current_title": self.current_title,
            "years_experience": self.years_experience,
            "resume_text": self.resume_text,
            "resume_pdf_path": self.resume_pdf_path,
            "resume_docx_path": self.resume_docx_path,
            "preferences": json.loads(self.preferences) if self.preferences else {},
            "target_companies": json.loads(self.target_companies) if self.target_companies else [],
            "blacklisted_companies": json.loads(self.blacklisted_companies) if self.blacklisted_companies else [],
            "notification_email": self.notification_email,
            "notification_telegram": self.notification_telegram,
            "telegram_chat_id": self.telegram_chat_id,
            "auto_analyze": self.auto_analyze,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class ResumeVersion(Base):
    """Multiple resume versions for different job targets"""
    __tablename__ = "resume_versions"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    version_name = Column(String, nullable=False)  # "Data Scientist Focus", "ML Engineer Focus"
    resume_text = Column(Text, nullable=False)
    resume_pdf_path = Column(String)
    focus_keywords = Column(Text)  # JSON array of emphasized skills
    target_roles = Column(Text)  # JSON array: ["Data Scientist", "ML Engineer"]
    created_at = Column(DateTime, default=func.now())
    is_active = Column(Boolean, default=True)
    
    def __repr__(self):
        return f"<ResumeVersion(id={self.id}, name='{self.version_name}')>"
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        import json
        return {
            "id": self.id,
            "version_name": self.version_name,
            "resume_text": self.resume_text,
            "resume_pdf_path": self.resume_pdf_path,
            "focus_keywords": json.loads(self.focus_keywords) if self.focus_keywords else [],
            "target_roles": json.loads(self.target_roles) if self.target_roles else [],
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "is_active": self.is_active,
        }


class CoverLetterTemplate(Base):
    """Cover letter templates with placeholders"""
    __tablename__ = "cover_letter_templates"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    template_name = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    placeholders = Column(Text)  # JSON: {company: "", role: "", project: ""}
    use_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=func.now())
    
    def __repr__(self):
        return f"<CoverLetterTemplate(id={self.id}, name='{self.template_name}')>"
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        import json
        return {
            "id": self.id,
            "template_name": self.template_name,
            "content": self.content,
            "placeholders": json.loads(self.placeholders) if self.placeholders else {},
            "use_count": self.use_count,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
