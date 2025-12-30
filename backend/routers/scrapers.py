"""
Scraper control endpoints
"""
from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from typing import Optional, List
from database import get_db
from scrapers.scraper_manager import ScraperManager
from utils.logger import setup_logger

router = APIRouter(prefix="/api/scrapers", tags=["scrapers"])
logger = setup_logger(__name__)


@router.post("/scrape")
def trigger_scraping(
    background_tasks: BackgroundTasks,
    keyword: str = "Data Scientist",
    location: str = "Germany",
    sources: Optional[List[str]] = None,
    db: Session = Depends(get_db)
):
    """
    Trigger job scraping
    
    - **keyword**: Search keyword (e.g., "Data Scientist", "Software Engineer")
    - **location**: Search location
    - **sources**: List of sources to scrape (None = all)
    """
    def run_scraping():
        manager = ScraperManager(db)
        stats = manager.scrape_all(keyword, location, sources)
        logger.info(f"Scraping completed: {stats}")
    
    background_tasks.add_task(run_scraping)
    
    return {
        "message": "Scraping started",
        "keyword": keyword,
        "location": location,
        "sources": sources or ["all"]
    }


@router.post("/scrape-companies")
def trigger_company_scraping(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Trigger company career page scraping"""
    def run_company_scraping():
        manager = ScraperManager(db)
        stats = manager.scrape_companies()
        logger.info(f"Company scraping completed: {stats}")
    
    background_tasks.add_task(run_company_scraping)
    
    return {"message": "Company scraping started"}


@router.get("/history")
def get_scraping_history(
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Get recent scraping history"""
    manager = ScraperManager(db)
    history = manager.get_scraping_history(limit)
    
    return {"history": history, "total": len(history)}


@router.get("/sources")
def get_available_sources():
    """Get list of available scraping sources"""
    return {
        "sources": [
            {"id": "arbeitsagentur", "name": "Arbeitsagentur", "type": "job_board"},
            {"id": "linkedin", "name": "LinkedIn", "type": "job_board"},
            {"id": "indeed", "name": "Indeed", "type": "job_board"},
            {"id": "stepstone", "name": "StepStone", "type": "job_board"},
            {"id": "glassdoor", "name": "Glassdoor", "type": "job_board"},
            {"id": "kimeta", "name": "Kimeta", "type": "aggregator"},
            {"id": "joblift", "name": "Joblift", "type": "aggregator"},
            {"id": "jooble", "name": "Jooble", "type": "aggregator"},
        ]
    }
