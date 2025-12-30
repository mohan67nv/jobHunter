"""
Application tracking endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from database import get_db
from models.application import Application
from models.job import Job
from schemas.application import ApplicationCreate, ApplicationUpdate, ApplicationResponse
from utils.logger import setup_logger

router = APIRouter(prefix="/api/applications", tags=["applications"])
logger = setup_logger(__name__)


@router.get("", response_model=List[ApplicationResponse])
def list_applications(
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    List all applications with optional status filter
    
    - **status**: Filter by status (saved, applied, interview, offer, rejected, etc.)
    """
    query = db.query(Application)
    
    if status:
        query = query.filter(Application.status == status)
    
    applications = query.order_by(Application.updated_at.desc()).all()
    
    return [app.to_dict() for app in applications]


@router.get("/stats")
def get_application_stats(db: Session = Depends(get_db)):
    """Get application statistics for dashboard"""
    
    # Count by status
    status_counts = {}
    statuses = ['saved', 'applied', 'phone_screen', 'interview', 'technical', 'offer', 'rejected', 'withdrawn']
    
    for status in statuses:
        count = db.query(Application).filter(Application.status == status).count()
        status_counts[status] = count
    
    # Recent activity
    recent = db.query(Application)\
        .order_by(Application.updated_at.desc())\
        .limit(10)\
        .all()
    
    # Upcoming interviews
    upcoming_interviews = db.query(Application)\
        .filter(Application.interview_date >= datetime.now())\
        .order_by(Application.interview_date)\
        .limit(5)\
        .all()
    
    return {
        "status_counts": status_counts,
        "total_applications": sum(status_counts.values()),
        "recent_activity": [app.to_dict() for app in recent],
        "upcoming_interviews": [app.to_dict() for app in upcoming_interviews]
    }


@router.post("", response_model=ApplicationResponse)
def create_application(
    application: ApplicationCreate,
    db: Session = Depends(get_db)
):
    """Create new application record"""
    
    # Verify job exists
    job = db.query(Job).get(application.job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Check if application already exists
    existing = db.query(Application).filter(Application.job_id == application.job_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Application already exists for this job")
    
    # Create application
    new_app = Application(**application.dict())
    db.add(new_app)
    db.commit()
    db.refresh(new_app)
    
    logger.info(f"Created application for job {application.job_id}")
    
    return new_app.to_dict()


@router.get("/{application_id}", response_model=ApplicationResponse)
def get_application(application_id: int, db: Session = Depends(get_db)):
    """Get single application by ID"""
    app = db.query(Application).get(application_id)
    
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    
    return app.to_dict()


@router.put("/{application_id}", response_model=ApplicationResponse)
def update_application(
    application_id: int,
    update_data: ApplicationUpdate,
    db: Session = Depends(get_db)
):
    """Update application status and details"""
    app = db.query(Application).get(application_id)
    
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    
    # Update fields
    update_dict = update_data.dict(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(app, key, value)
    
    app.updated_at = datetime.now()
    db.commit()
    db.refresh(app)
    
    logger.info(f"Updated application {application_id}: status={app.status}")
    
    return app.to_dict()


@router.delete("/{application_id}")
def delete_application(application_id: int, db: Session = Depends(get_db)):
    """Delete application"""
    app = db.query(Application).get(application_id)
    
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    
    db.delete(app)
    db.commit()
    
    return {"message": "Application deleted successfully"}
