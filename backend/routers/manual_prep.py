"""
Manual Prep API Router
Endpoints for manually created interview preparation sessions
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from database import get_db
from models.manual_prep import ManualPrep
from models.user import UserProfile
from ai_agents.manual_prep_agent import ManualPrepAgent
from utils.logger import setup_logger
import json

router = APIRouter(prefix="/api/manual-prep", tags=["manual-prep"])
logger = setup_logger(__name__)

# Initialize AI agent
prep_agent = ManualPrepAgent()


@router.post("", status_code=201)
async def create_manual_prep(
    company_name: str,
    job_url: Optional[str] = None,
    job_title: Optional[str] = None,
    job_description: Optional[str] = None,
    user_id: int = 1,  # TODO: Get from auth
    db: Session = Depends(get_db)
):
    """
    Create new manual interview preparation
    Generates advanced AI content using DeepSeek models
    """
    try:
        logger.info(f"📝 Creating manual prep: {company_name} - {job_title}")
        
        # Get user's resume if available
        user = db.query(UserProfile).filter(UserProfile.id == user_id).first()
        resume_text = user.resume_text if user else None
        
        # Generate AI content using DeepSeek models
        logger.info("🤖 Generating AI content...")
        ai_results = prep_agent.process(
            company_name=company_name,
            job_title=job_title,
            job_description=job_description,
            job_url=job_url,
            resume_text=resume_text
        )
        
        # Create database entry
        manual_prep = ManualPrep(
            user_id=user_id,
            company_name=company_name,
            job_url=job_url,
            job_title=job_title or "Position at " + company_name,
            job_description=job_description,
            company_insights=json.dumps(ai_results.get('company_insights', {})),
            technical_qa=json.dumps(ai_results.get('technical_qa', [])),
            behavioral_qa=json.dumps(ai_results.get('behavioral_qa', [])),
            hr_qa=json.dumps(ai_results.get('hr_qa', [])),
            key_talking_points=json.dumps(ai_results.get('key_talking_points', [])),
            preparation_tips=json.dumps(ai_results.get('preparation_tips', [])),
            expires_at=datetime.utcnow() + timedelta(days=30),
            status="active"
        )
        
        db.add(manual_prep)
        db.commit()
        db.refresh(manual_prep)
        
        logger.info(f"✅ Manual prep created: ID {manual_prep.id}")
        
        return {
            "id": manual_prep.id,
            "message": "Manual prep created successfully",
            "data": manual_prep.to_dict()
        }
        
    except Exception as e:
        logger.error(f"❌ Error creating manual prep: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("")
async def get_manual_preps(
    status: Optional[str] = Query(None, description="Filter by status: active/archived/completed"),
    search: Optional[str] = Query(None, description="Search company or job title"),
    include_expired: bool = Query(False, description="Include expired preps"),
    user_id: int = 1,  # TODO: Get from auth
    db: Session = Depends(get_db)
):
    """
    Get all manual preps for user
    Supports filtering and search
    """
    try:
        query = db.query(ManualPrep).filter(ManualPrep.user_id == user_id)
        
        # Filter by status
        if status:
            query = query.filter(ManualPrep.status == status)
        
        # Exclude expired unless requested
        if not include_expired:
            query = query.filter(ManualPrep.expires_at > datetime.utcnow())
        
        # Search filter
        if search:
            search_pattern = f"%{search}%"
            query = query.filter(
                (ManualPrep.company_name.ilike(search_pattern)) |
                (ManualPrep.job_title.ilike(search_pattern))
            )
        
        # Order by creation date
        preps = query.order_by(ManualPrep.created_at.desc()).all()
        
        return {
            "count": len(preps),
            "data": [prep.to_dict() for prep in preps]
        }
        
    except Exception as e:
        logger.error(f"❌ Error fetching manual preps: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{prep_id}")
async def get_manual_prep(
    prep_id: int,
    user_id: int = 1,  # TODO: Get from auth
    db: Session = Depends(get_db)
):
    """Get single manual prep by ID"""
    try:
        prep = db.query(ManualPrep).filter(
            ManualPrep.id == prep_id,
            ManualPrep.user_id == user_id
        ).first()
        
        if not prep:
            raise HTTPException(status_code=404, detail="Manual prep not found")
        
        return prep.to_dict()
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error fetching manual prep {prep_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{prep_id}")
async def update_manual_prep(
    prep_id: int,
    status: Optional[str] = None,
    interview_date: Optional[datetime] = None,
    is_favorite: Optional[bool] = None,
    user_notes: Optional[str] = None,
    user_id: int = 1,  # TODO: Get from auth
    db: Session = Depends(get_db)
):
    """
    Update manual prep
    Can update status, interview date, favorite, notes
    """
    try:
        prep = db.query(ManualPrep).filter(
            ManualPrep.id == prep_id,
            ManualPrep.user_id == user_id
        ).first()
        
        if not prep:
            raise HTTPException(status_code=404, detail="Manual prep not found")
        
        # Update fields
        if status is not None:
            if status not in ['active', 'archived', 'completed']:
                raise HTTPException(status_code=400, detail="Invalid status")
            prep.status = status
        
        if interview_date is not None:
            prep.interview_date = interview_date
        
        if is_favorite is not None:
            prep.is_favorite = is_favorite
        
        if user_notes is not None:
            prep.user_notes = user_notes
        
        prep.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(prep)
        
        logger.info(f"✅ Updated manual prep {prep_id}")
        
        return {
            "message": "Manual prep updated successfully",
            "data": prep.to_dict()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error updating manual prep {prep_id}: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{prep_id}")
async def delete_manual_prep(
    prep_id: int,
    user_id: int = 1,  # TODO: Get from auth
    db: Session = Depends(get_db)
):
    """Delete manual prep (hard delete)"""
    try:
        prep = db.query(ManualPrep).filter(
            ManualPrep.id == prep_id,
            ManualPrep.user_id == user_id
        ).first()
        
        if not prep:
            raise HTTPException(status_code=404, detail="Manual prep not found")
        
        db.delete(prep)
        db.commit()
        
        logger.info(f"🗑️ Deleted manual prep {prep_id}")
        
        return {"message": "Manual prep deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error deleting manual prep {prep_id}: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/cleanup")
async def cleanup_expired_preps(
    user_id: int = 1,  # TODO: Get from auth
    db: Session = Depends(get_db)
):
    """
    Cleanup expired manual preps (auto-delete after 30 days)
    Archives instead of hard delete
    """
    try:
        now = datetime.utcnow()
        
        expired_preps = db.query(ManualPrep).filter(
            ManualPrep.user_id == user_id,
            ManualPrep.expires_at <= now,
            ManualPrep.status == 'active'
        ).all()
        
        count = 0
        for prep in expired_preps:
            prep.status = 'archived'
            count += 1
        
        db.commit()
        
        logger.info(f"🧹 Archived {count} expired manual preps")
        
        return {
            "message": f"Archived {count} expired preparations",
            "count": count
        }
        
    except Exception as e:
        logger.error(f"❌ Error cleaning up expired preps: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{prep_id}/regenerate")
async def regenerate_prep_content(
    prep_id: int,
    section: Optional[str] = Query(None, description="Specific section to regenerate: technical_qa/behavioral_qa/hr_qa/company_insights/all"),
    user_id: int = 1,  # TODO: Get from auth
    db: Session = Depends(get_db)
):
    """
    Regenerate AI content for manual prep
    Useful if user wants fresh insights
    """
    try:
        prep = db.query(ManualPrep).filter(
            ManualPrep.id == prep_id,
            ManualPrep.user_id == user_id
        ).first()
        
        if not prep:
            raise HTTPException(status_code=404, detail="Manual prep not found")
        
        # Get user's resume
        user = db.query(UserProfile).filter(UserProfile.id == user_id).first()
        resume_text = user.resume_text if user else None
        
        # Regenerate content
        logger.info(f"🔄 Regenerating content for prep {prep_id}, section: {section or 'all'}")
        
        ai_results = prep_agent.process(
            company_name=prep.company_name,
            job_title=prep.job_title,
            job_description=prep.job_description,
            job_url=prep.job_url,
            resume_text=resume_text
        )
        
        # Update specified section or all
        if not section or section == 'all':
            prep.company_insights = json.dumps(ai_results.get('company_insights', {}))
            prep.technical_qa = json.dumps(ai_results.get('technical_qa', []))
            prep.behavioral_qa = json.dumps(ai_results.get('behavioral_qa', []))
            prep.hr_qa = json.dumps(ai_results.get('hr_qa', []))
            prep.key_talking_points = json.dumps(ai_results.get('key_talking_points', []))
            prep.preparation_tips = json.dumps(ai_results.get('preparation_tips', []))
        else:
            if section in ai_results:
                setattr(prep, section, json.dumps(ai_results[section]))
        
        prep.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(prep)
        
        logger.info(f"✅ Regenerated content for prep {prep_id}")
        
        return {
            "message": "Content regenerated successfully",
            "data": prep.to_dict()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error regenerating prep content {prep_id}: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats/summary")
async def get_prep_stats(
    user_id: int = 1,  # TODO: Get from auth
    db: Session = Depends(get_db)
):
    """Get statistics about user's manual preps"""
    try:
        total = db.query(ManualPrep).filter(ManualPrep.user_id == user_id).count()
        active = db.query(ManualPrep).filter(
            ManualPrep.user_id == user_id,
            ManualPrep.status == 'active'
        ).count()
        completed = db.query(ManualPrep).filter(
            ManualPrep.user_id == user_id,
            ManualPrep.status == 'completed'
        ).count()
        archived = db.query(ManualPrep).filter(
            ManualPrep.user_id == user_id,
            ManualPrep.status == 'archived'
        ).count()
        
        upcoming = db.query(ManualPrep).filter(
            ManualPrep.user_id == user_id,
            ManualPrep.interview_date != None,
            ManualPrep.interview_date > datetime.utcnow()
        ).count()
        
        return {
            "total": total,
            "active": active,
            "completed": completed,
            "archived": archived,
            "upcoming_interviews": upcoming
        }
        
    except Exception as e:
        logger.error(f"❌ Error fetching prep stats: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
