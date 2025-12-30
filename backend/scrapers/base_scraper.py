"""
Base scraper class - abstract interface for all scrapers
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Optional
import time
import random
from datetime import datetime
from utils.logger import setup_logger

logger = setup_logger(__name__)


class BaseScraper(ABC):
    """Abstract base class for all job scrapers"""
    
    def __init__(self, delay_min: int = 2, delay_max: int = 5):
        """
        Initialize scraper
        
        Args:
            delay_min: Minimum delay between requests (seconds)
            delay_max: Maximum delay between requests (seconds)
        """
        self.delay_min = delay_min
        self.delay_max = delay_max
        self.source_name = self.__class__.__name__.replace("Scraper", "")
        self.logger = logger
    
    @abstractmethod
    def scrape(self, keyword: str, location: str = "Germany", **kwargs) -> List[Dict]:
        """
        Scrape jobs from source
        
        Args:
            keyword: Job search keyword (e.g., "Data Scientist")
            location: Location to search in
            **kwargs: Additional scraper-specific parameters
            
        Returns:
            List of job dictionaries with standardized fields
        """
        pass
    
    def random_delay(self):
        """Add random delay between requests to avoid rate limiting"""
        delay = random.uniform(self.delay_min, self.delay_max)
        self.logger.debug(f"Waiting {delay:.2f} seconds before next request...")
        time.sleep(delay)
    
    def normalize_job(self, raw_job: Dict) -> Dict:
        """
        Normalize job data to standard format
        
        Expected fields:
        - title (required)
        - company (required)
        - location (required)
        - description (required)
        - url (required)
        - posted_date (required, datetime)
        - salary (optional)
        - job_type (optional)
        - contract_type (optional)
        - remote_type (optional)
        - experience_level (optional)
        - requirements (optional)
        - benefits (optional)
        """
        normalized = {
            "title": raw_job.get("title", "").strip(),
            "company": raw_job.get("company", "").strip(),
            "location": raw_job.get("location", "").strip(),
            "description": raw_job.get("description", "").strip(),
            "url": raw_job.get("url", "").strip(),
            "posted_date": raw_job.get("posted_date", datetime.now()),
            "salary": raw_job.get("salary"),
            "job_type": raw_job.get("job_type"),
            "contract_type": raw_job.get("contract_type"),
            "remote_type": raw_job.get("remote_type"),
            "experience_level": raw_job.get("experience_level"),
            "requirements": raw_job.get("requirements"),
            "benefits": raw_job.get("benefits"),
            "source": self.source_name,
            "scraped_date": datetime.now(),
        }
        return normalized
    
    def validate_job(self, job: Dict) -> bool:
        """
        Validate that job has all required fields
        
        Args:
            job: Job dictionary to validate
            
        Returns:
            True if valid, False otherwise
        """
        required_fields = ["title", "company", "location", "description", "url"]
        
        for field in required_fields:
            if not job.get(field):
                self.logger.warning(f"Job missing required field '{field}': {job.get('title', 'Unknown')}")
                return False
        
        return True
    
    def log_scraping_stats(self, jobs: List[Dict]):
        """Log scraping statistics"""
        self.logger.info(f"✅ {self.source_name}: Scraped {len(jobs)} jobs")
        
        if jobs:
            companies = set(job.get("company") for job in jobs)
            locations = set(job.get("location") for job in jobs)
            self.logger.info(f"   Companies: {len(companies)}, Locations: {len(locations)}")
