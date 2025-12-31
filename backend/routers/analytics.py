"""
Analytics and statistics endpoints
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import datetime, timedelta
from database import get_db
from models.job import Job, JobAnalysis
from models.application import Application
from models.scraping_log import ScrapingLog
from utils.logger import setup_logger

router = APIRouter(prefix="/api/analytics", tags=["analytics"])
logger = setup_logger(__name__)


@router.get("/overview")
def get_overview(db: Session = Depends(get_db)):
    """Get dashboard overview statistics"""
    
    # Total jobs
    total_jobs = db.query(Job).filter(Job.is_active == True, Job.is_duplicate == False).count()
    
    # New jobs today (exclude duplicates)
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    new_today = db.query(Job).filter(
        Job.scraped_date >= today,
        Job.is_active == True,
        Job.is_duplicate == False
    ).count()
    
    # High match jobs (80%+)
    high_match = db.query(Job).join(JobAnalysis).filter(
        Job.is_active == True,
        JobAnalysis.match_score >= 80
    ).count()
    
    # Total applications
    total_applications = db.query(Application).count()
    
    # Applications by status
    active_applications = db.query(Application).filter(
        Application.status.in_(['applied', 'phone_screen', 'interview', 'technical'])
    ).count()
    
    # Recent scraping activity
    last_scrape = db.query(ScrapingLog).order_by(ScrapingLog.started_at.desc()).first()
    
    return {
        "total_jobs": total_jobs,
        "new_today": new_today,
        "high_match_jobs": high_match,
        "total_applications": total_applications,
        "active_applications": active_applications,
        "last_scrape": last_scrape.to_dict() if last_scrape else None
    }


@router.get("/applications-timeline")
def get_applications_timeline(days: int = 30, db: Session = Depends(get_db)):
    """Get application counts over time"""
    
    start_date = datetime.now() - timedelta(days=days)
    
    # Group by date
    timeline = db.query(
        func.date(Application.created_at).label('date'),
        func.count(Application.id).label('count')
    ).filter(
        Application.created_at >= start_date
    ).group_by(
        func.date(Application.created_at)
    ).order_by('date').all()
    
    return {
        "timeline": [{"date": str(t.date), "count": t.count} for t in timeline]
    }


@router.get("/sources")
def get_jobs_by_source(db: Session = Depends(get_db)):
    """Get job count by source"""
    
    sources = db.query(
        Job.source,
        func.count(Job.id).label('count')
    ).filter(
        Job.is_active == True,
        Job.is_duplicate == False
    ).group_by(Job.source).all()
    
    return {
        "sources": [{"source": s.source, "count": s.count} for s in sources]
    }


@router.get("/match-score-distribution")
def get_match_score_distribution(db: Session = Depends(get_db)):
    """Get distribution of match scores"""
    
    # Group by score ranges
    ranges = [
        (0, 60, "Low"),
        (60, 80, "Medium"),
        (80, 90, "High"),
        (90, 100, "Excellent")
    ]
    
    distribution = []
    
    for min_score, max_score, label in ranges:
        count = db.query(JobAnalysis).filter(
            JobAnalysis.match_score >= min_score,
            JobAnalysis.match_score < max_score
        ).count()
        
        distribution.append({
            "range": label,
            "min": min_score,
            "max": max_score,
            "count": count
        })
    
    return {"distribution": distribution}


@router.get("/top-companies")
def get_top_companies(limit: int = 10, db: Session = Depends(get_db)):
    """Get companies with most job postings"""
    
    companies = db.query(
        Job.company,
        func.count(Job.id).label('job_count')
    ).filter(
        Job.is_active == True,
        Job.is_duplicate == False
    ).group_by(Job.company).order_by(desc('job_count')).limit(limit).all()
    
    return {
        "companies": [{"company": c.company, "job_count": c.job_count} for c in companies]
    }


@router.get("/skills-demand")
def get_skills_in_demand(limit: int = 20, db: Session = Depends(get_db)):
    """Get most in-demand skills from job postings"""
    
    # This is a simplified version - in production, you'd parse job descriptions
    # and count skill occurrences
    
    # Get all job analyses with required skills
    analyses = db.query(JobAnalysis).limit(1000).all()
    
    skill_counts = {}
    
    for analysis in analyses:
        import json
        skills = json.loads(analysis.matching_skills) if analysis.matching_skills else []
        for skill in skills:
            skill_counts[skill] = skill_counts.get(skill, 0) + 1
    
    # Sort by count
    sorted_skills = sorted(skill_counts.items(), key=lambda x: x[1], reverse=True)[:limit]
    
    return {
        "skills": [{"skill": skill, "count": count} for skill, count in sorted_skills]
    }


@router.get("/application-funnel")
def get_application_funnel(db: Session = Depends(get_db)):
    """Get application funnel statistics"""
    
    # Count by each stage
    saved = db.query(Application).filter(Application.status == 'saved').count()
    applied = db.query(Application).filter(Application.status == 'applied').count()
    phone_screen = db.query(Application).filter(Application.status == 'phone_screen').count()
    interview = db.query(Application).filter(Application.status == 'interview').count()
    technical = db.query(Application).filter(Application.status == 'technical').count()
    offer = db.query(Application).filter(Application.status == 'offer').count()
    
    return {
        "funnel": [
            {"stage": "Saved", "count": saved},
            {"stage": "Applied", "count": applied},
            {"stage": "Phone Screen", "count": phone_screen},
            {"stage": "Interview", "count": interview},
            {"stage": "Technical", "count": technical},
            {"stage": "Offer", "count": offer}
        ]
    }


@router.get("/success-rate")
def get_success_rate_by_source(db: Session = Depends(get_db)):
    """Get application success rate by job source"""
    
    # This would calculate conversion rates from application to offer by source
    # Simplified version for now
    
    sources = db.query(Job.source).distinct().all()
    
    stats = []
    
    for (source,) in sources:
        # Get jobs from this source with applications
        jobs = db.query(Job).filter(Job.source == source).all()
        job_ids = [j.id for j in jobs]
        
        if not job_ids:
            continue
        
        total_apps = db.query(Application).filter(Application.job_id.in_(job_ids)).count()
        offers = db.query(Application).filter(
            Application.job_id.in_(job_ids),
            Application.status == 'offer'
        ).count()
        
        success_rate = (offers / total_apps * 100) if total_apps > 0 else 0
        
        stats.append({
            "source": source,
            "applications": total_apps,
            "offers": offers,
            "success_rate": round(success_rate, 2)
        })
    
    return {"stats": stats}
