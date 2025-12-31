"""
Application model - tracks job application status
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class Application(Base):
    """Application tracking model"""
    __tablename__ = "applications"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    job_id = Column(Integer, ForeignKey('jobs.id', ondelete='CASCADE'), nullable=False)
    status = Column(String, nullable=False, default='saved', index=True)
    # Status values: saved, applied, phone_screen, interview, technical, offer, rejected, withdrawn
    applied_date = Column(DateTime)
    interview_date = Column(DateTime)
    interview_type = Column(String)  # phone, video, on-site, technical
    follow_up_date = Column(DateTime)
    notes = Column(Text)
    resume_version = Column(String)  # Which resume version was used
    cover_letter_used = Column(String)  # Which cover letter template
    salary_expectation = Column(String)
    rejection_reason = Column(Text)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    job = relationship("Job", back_populates="applications")
    
    def __repr__(self):
        return f"<Application(id={self.id}, job_id={self.job_id}, status='{self.status}')>"
    
    def to_dict(self, include_job=False):
        """Convert to dictionary for API responses"""
        data = {
            "id": self.id,
            "job_id": self.job_id,
            "status": self.status,
            "applied_date": self.applied_date.isoformat() if self.applied_date else None,
            "interview_date": self.interview_date.isoformat() if self.interview_date else None,
            "interview_type": self.interview_type,
            "follow_up_date": self.follow_up_date.isoformat() if self.follow_up_date else None,
            "notes": self.notes,
            "resume_version": self.resume_version,
            "cover_letter_used": self.cover_letter_used,
            "salary_expectation": self.salary_expectation,
            "rejection_reason": self.rejection_reason,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
        
        # Include job details if requested
        if include_job and self.job:
            data['job'] = {
                'id': self.job.id,
                'title': self.job.title,
                'company': self.job.company,
                'location': self.job.location,
                'url': self.job.url,
                'source': self.job.source,
            }
        
        return data


# Create indexes
Index('idx_applications_status', Application.status)
Index('idx_applications_dates', Application.applied_date, Application.interview_date)
