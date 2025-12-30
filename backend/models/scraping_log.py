"""
Scraping log model - tracks scraping sessions
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Index
from sqlalchemy.sql import func
from database import Base


class ScrapingLog(Base):
    """Scraping session logs"""
    __tablename__ = "scraping_logs"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    source = Column(String, nullable=False, index=True)  # LinkedIn, Kimeta, BMW Careers
    jobs_found = Column(Integer, default=0)
    jobs_new = Column(Integer, default=0)
    jobs_updated = Column(Integer, default=0)
    status = Column(String)  # success, partial, failed
    error_message = Column(Text)
    duration_seconds = Column(Float)
    started_at = Column(DateTime, nullable=False, index=True)
    completed_at = Column(DateTime)
    
    def __repr__(self):
        return f"<ScrapingLog(id={self.id}, source='{self.source}', status='{self.status}')>"
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            "id": self.id,
            "source": self.source,
            "jobs_found": self.jobs_found,
            "jobs_new": self.jobs_new,
            "jobs_updated": self.jobs_updated,
            "status": self.status,
            "error_message": self.error_message,
            "duration_seconds": self.duration_seconds,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }


# Create indexes
Index('idx_logs_source', ScrapingLog.source)
Index('idx_logs_date', ScrapingLog.started_at.desc())
