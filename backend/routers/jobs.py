"""
Job endpoints - CRUD operations for jobs
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload, contains_eager
from typing import List, Optional
from datetime import datetime, timedelta
from database import get_db
from models.job import Job, JobAnalysis
from schemas.job import JobResponse, JobListResponse
from utils.logger import setup_logger

router = APIRouter(prefix="/api/jobs", tags=["jobs"])
logger = setup_logger(__name__)


@router.get("", response_model=JobListResponse)
def list_jobs(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    source: Optional[str] = None,
    job_type: Optional[str] = None,
    remote_type: Optional[str] = None,
    experience_level: Optional[str] = None,
    min_match_score: Optional[float] = None,
    posted_after: Optional[str] = None,
    search: Optional[str] = None,
    include_duplicates: bool = False,
    db: Session = Depends(get_db)
):
    """
    List jobs with filtering and pagination
    
    - **page**: Page number (1-indexed)
    - **page_size**: Number of jobs per page
    - **source**: Filter by source (LinkedIn, Indeed, etc.)
    - **job_type**: Filter by job type (full-time, contract, etc.)
    - **remote_type**: Filter by remote type (remote, hybrid, on-site)
    - **experience_level**: Filter by experience level (entry, mid, senior, lead)
    - **min_match_score**: Minimum match score (0-100)
    - **posted_after**: ISO date string (e.g., "2024-01-01")
    - **search**: Search in title, company, location
    - **include_duplicates**: Include duplicate jobs
    """
    query = db.query(Job).filter(Job.is_active == True)
    
    # Apply filters
    if not include_duplicates:
        query = query.filter(Job.is_duplicate == False)
    
    if source:
        query = query.filter(Job.source == source)
    
    if job_type:
        query = query.filter(Job.job_type == job_type)
    
    if remote_type:
        query = query.filter(Job.remote_type == remote_type)
    
    if experience_level:
        query = query.filter(Job.experience_level == experience_level)
    
    if posted_after:
        try:
            date = datetime.fromisoformat(posted_after)
            query = query.filter(Job.posted_date >= date)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format")
    
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (Job.title.ilike(search_term)) |
            (Job.company.ilike(search_term)) |
            (Job.location.ilike(search_term))
        )
    
    # Filter by match score if provided
    if min_match_score is not None:
        # Use subquery to filter, then eager load analysis
        query = query.filter(
            Job.id.in_(
                db.query(Job.id)
                .join(JobAnalysis)
                .filter(JobAnalysis.match_score >= min_match_score)
            )
        )
    
    # Always eager load analysis for all results
    query = query.options(joinedload(Job.analysis))
    
    # Get total count (all matching jobs in database)
    total = query.count()
    logger.info(f"📊 Found {total} jobs in database (page {page}, size {page_size})")
    
    # Apply pagination and sorting
    jobs = query.order_by(Job.posted_date.desc())\
        .offset((page - 1) * page_size)\
        .limit(page_size)\
        .all()
    
    # Convert jobs to dict and add match_score from analysis if exists
    jobs_list = []
    for job in jobs:
        job_dict = job.to_dict()
        # Add match score from analysis if available
        if job.analysis:
            job_dict['match_score'] = job.analysis.match_score
            job_dict['ats_score'] = job.analysis.ats_score
        else:
            job_dict['match_score'] = None
            job_dict['ats_score'] = None
        jobs_list.append(job_dict)
    
    return JobListResponse(
        jobs=jobs_list,
        total=total,
        page=page,
        page_size=page_size
    )


@router.get("/{job_id}", response_model=JobResponse)
def get_job(job_id: int, db: Session = Depends(get_db)):
    """Get single job by ID"""
    job = db.query(Job).get(job_id)
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Increment view count
    job.view_count += 1
    db.commit()
    
    return job.to_dict()


@router.put("/{job_id}")
def update_job(job_id: int, is_active: Optional[bool] = None, db: Session = Depends(get_db)):
    """Update job (e.g., mark as inactive)"""
    job = db.query(Job).get(job_id)
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    if is_active is not None:
        job.is_active = is_active
    
    job.updated_at = datetime.now()
    db.commit()
    
    return {"message": "Job updated successfully", "job": job.to_dict()}


@router.delete("/{job_id}")
def delete_job(job_id: int, db: Session = Depends(get_db)):
    """Delete job"""
    job = db.query(Job).get(job_id)
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    db.delete(job)
    db.commit()
    
    return {"message": "Job deleted successfully"}


@router.get("/{job_id}/similar")
def get_similar_jobs(job_id: int, limit: int = 10, db: Session = Depends(get_db)):
    """Get similar jobs based on company and title"""
    job = db.query(Job).get(job_id)
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Find similar jobs (same company or similar title)
    similar = db.query(Job).filter(
        Job.id != job_id,
        Job.is_active == True,
        Job.is_duplicate == False,
        (Job.company == job.company) | (Job.title.ilike(f"%{job.title[:20]}%"))
    ).limit(limit).all()
    
    return {"similar_jobs": [j.to_dict() for j in similar]}
