"""
Scraper control endpoints
"""
from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime
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
        
        # Calculate match scores for newly scraped jobs (for filtering)
        from ai_agents.quick_matcher import QuickMatcher
        from models.user import UserProfile
        from models.job import Job, JobAnalysis
        
        user = db.query(UserProfile).first()
        if user and user.resume_text:
            quick_matcher = QuickMatcher()
            
            # Get unmatched jobs
            unmatched_jobs = db.query(Job)\
                .outerjoin(JobAnalysis)\
                .filter(JobAnalysis.id == None)\
                .limit(100)\
                .all()
            
            if unmatched_jobs:
                logger.info(f"🎯 Calculating match scores for {len(unmatched_jobs)} new jobs...")
                
                for job in unmatched_jobs:
                    try:
                        # Quick match score (for filtering only)
                        score = quick_matcher.calculate_quick_match(
                            user.resume_text,
                            job.description or "",
                            job.title
                        )
                        
                        # Create lightweight analysis with ONLY match_score
                        # ATS score requires full AI analysis (user clicks "Run AI Analysis")
                        analysis = JobAnalysis(
                            job_id=job.id,
                            match_score=score,
                            ats_score=0,  # Not calculated yet - requires full analysis
                            matching_skills="[]",
                            missing_skills="[]",
                            recommendations="{}",
                            analyzed_at=datetime.now()
                        )
                        db.add(analysis)
                    except Exception as e:
                        logger.error(f"Error calculating match score for job {job.id}: {e}")
                
                db.commit()
                logger.info(f"✅ Match scores calculated - jobs ready for filtering!")
    
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
    from job_sources import ALL_JOB_SOURCES, RECOMMENDED_COMBINATIONS
    
    sources_list = []
    for source_id, details in ALL_JOB_SOURCES.items():
        sources_list.append({
            "id": source_id,
            "name": details['name'],
            "type": details['type'],
            "description": details['description'],
            "active": details['active'],
            "priority": details['priority'],
        })
    
    return {
        "sources": sources_list,
        "total": len(sources_list),
        "recommended_combinations": RECOMMENDED_COMBINATIONS,
        "currently_implemented": ["arbeitsagentur", "kimeta", "joblift", "jooble", "indeed", "linkedin", "stepstone", "glassdoor"]
    }

