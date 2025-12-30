"""
Company model - tracks companies for career page scraping
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float, Index
from sqlalchemy.sql import func
from database import Base


class Company(Base):
    """Company database for career page scraping"""
    __tablename__ = "companies"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True, index=True)
    career_url = Column(String, nullable=False)
    logo_url = Column(String)
    industry = Column(String, index=True)
    size = Column(String)  # "1-50", "51-200", "201-1000", "1000+"
    glassdoor_rating = Column(Float)
    glassdoor_url = Column(String)
    location = Column(String)
    description = Column(Text)
    last_scraped = Column(DateTime)
    scrape_frequency = Column(String, default='daily')  # daily, weekly, monthly
    is_active = Column(Boolean, default=True)
    notes = Column(Text)
    
    def __repr__(self):
        return f"<Company(id={self.id}, name='{self.name}')>"
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            "id": self.id,
            "name": self.name,
            "career_url": self.career_url,
            "logo_url": self.logo_url,
            "industry": self.industry,
            "size": self.size,
            "glassdoor_rating": self.glassdoor_rating,
            "glassdoor_url": self.glassdoor_url,
            "location": self.location,
            "description": self.description,
            "last_scraped": self.last_scraped.isoformat() if self.last_scraped else None,
            "scrape_frequency": self.scrape_frequency,
            "is_active": self.is_active,
            "notes": self.notes,
        }


# Create indexes
Index('idx_companies_name', Company.name)
Index('idx_companies_industry', Company.industry)
