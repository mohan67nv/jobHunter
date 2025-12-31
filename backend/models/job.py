"""
Job and JobAnalysis models
Core tables for storing scraped jobs and AI analysis results
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float, ForeignKey, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class Job(Base):
    """Job posting model - stores all scraped job data"""
    __tablename__ = "jobs"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False, index=True)
    company = Column(String, nullable=False, index=True)
    location = Column(String, nullable=False)
    salary = Column(String)  # e.g., "€70,000 - €90,000"
    job_type = Column(String)  # full-time, contract, freelance, internship
    contract_type = Column(String)  # permanent, temporary, freelance
    remote_type = Column(String)  # on-site, hybrid, remote
    experience_level = Column(String)  # entry, mid, senior, lead
    posted_date = Column(DateTime, nullable=False, index=True)
    scraped_date = Column(DateTime, default=func.now())
    deadline_date = Column(DateTime)
    description = Column(Text, nullable=False)
    requirements = Column(Text)
    benefits = Column(Text)
    url = Column(String, nullable=False, unique=True, index=True)
    source = Column(String, nullable=False, index=True)  # LinkedIn, BMW Careers, Kimeta, etc.
    is_active = Column(Boolean, default=True, index=True)
    is_duplicate = Column(Boolean, default=False)
    duplicate_of = Column(Integer, ForeignKey('jobs.id'))
    view_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    analysis = relationship("JobAnalysis", back_populates="job", uselist=False, cascade="all, delete-orphan")
    applications = relationship("Application", back_populates="job", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Job(id={self.id}, title='{self.title}', company='{self.company}')>"
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        # Extract languages from requirements if available
        languages = []
        if self.requirements:
            req_lower = self.requirements.lower()
            if 'english' in req_lower:
                languages.append('English')
            if 'german' in req_lower and 'fluent' not in req_lower:
                languages.append('German (basic/intermediate)')
        
        return {
            "id": self.id,
            "title": self.title,
            "languages": languages,
            "company": self.company,
            "location": self.location,
            "salary": self.salary,
            "job_type": self.job_type,
            "contract_type": self.contract_type,
            "remote_type": self.remote_type,
            "experience_level": self.experience_level,
            "posted_date": self.posted_date.isoformat() if self.posted_date else None,
            "scraped_date": self.scraped_date.isoformat() if self.scraped_date else None,
            "deadline_date": self.deadline_date.isoformat() if self.deadline_date else None,
            "description": self.description,
            "requirements": self.requirements,
            "benefits": self.benefits,
            "url": self.url,
            "source": self.source,
            "is_active": self.is_active,
            "is_duplicate": self.is_duplicate,
            "duplicate_of": self.duplicate_of,
            "view_count": self.view_count,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class JobAnalysis(Base):
    """AI analysis results for jobs"""
    __tablename__ = "job_analysis"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    job_id = Column(Integer, ForeignKey('jobs.id', ondelete='CASCADE'), nullable=False, index=True)
    match_score = Column(Float)  # 0-100
    ats_score = Column(Float)  # 0-100
    matching_skills = Column(Text)  # JSON array: ["Python", "SQL", "AWS"]
    missing_skills = Column(Text)  # JSON array: ["Kubernetes", "Terraform"]
    experience_match = Column(String)  # "Perfect", "Close", "Gap"
    salary_match = Column(String)  # "Above", "Match", "Below", "Unknown"
    keyword_density = Column(Float)  # Percentage of resume keywords in JD
    recommendations = Column(Text)  # JSON: {resume: [...], cover_letter: [...]}
    tailored_resume = Column(Text)  # Generated resume bullets
    tailored_cover_letter = Column(Text)  # Generated cover letter
    interview_questions = Column(Text)  # JSON array of likely questions
    analyzed_at = Column(DateTime, default=func.now())
    
    # Relationships
    job = relationship("Job", back_populates="analysis")
    
    def __repr__(self):
        return f"<JobAnalysis(job_id={self.job_id}, match_score={self.match_score})>"
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        import json
        
        # Helper to parse JSON or return default
        def safe_json_parse(value, default):
            if not value:
                return default
            try:
                return json.loads(value)
            except (json.JSONDecodeError, TypeError):
                # If it's a plain string, try to convert to appropriate type
                if isinstance(default, list):
                    # Split comma-separated string
                    return [s.strip() for s in value.split(',') if s.strip()]
                elif isinstance(default, dict):
                    return {"general": value} if value else {}
                return default
        
        return {
            "id": self.id,
            "job_id": self.job_id,
            "match_score": self.match_score,
            "ats_score": self.ats_score,
            "matching_skills": safe_json_parse(self.matching_skills, []),
            "missing_skills": safe_json_parse(self.missing_skills, []),
            "experience_match": self.experience_match,
            "salary_match": self.salary_match,
            "keyword_density": self.keyword_density,
            "recommendations": safe_json_parse(self.recommendations, {}),
            "tailored_resume": self.tailored_resume,
            "tailored_cover_letter": self.tailored_cover_letter,
            "interview_questions": safe_json_parse(self.interview_questions, []),
            "analyzed_at": self.analyzed_at.isoformat() if self.analyzed_at else None,
        }


# Create indexes
Index('idx_jobs_company', Job.company)
Index('idx_jobs_posted_date', Job.posted_date.desc())
Index('idx_jobs_source', Job.source)
Index('idx_jobs_active', Job.is_active)
Index('idx_analysis_job', JobAnalysis.job_id)
Index('idx_analysis_match_score', JobAnalysis.match_score.desc())
