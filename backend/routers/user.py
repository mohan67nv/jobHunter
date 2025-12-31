"""
User profile endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import Optional
import os
import json
from datetime import datetime
from database import get_db
from models.user import UserProfile, ResumeVersion, CoverLetterTemplate
from schemas.user import UserProfileUpdate, UserProfileResponse
from utils.parser import ResumeParser
from utils.logger import setup_logger

router = APIRouter(prefix="/api/user", tags=["user"])
logger = setup_logger(__name__)


@router.get("/profile", response_model=UserProfileResponse)
def get_profile(db: Session = Depends(get_db)):
    """Get user profile"""
    user = db.query(UserProfile).filter(UserProfile.id == 1).first()
    
    if not user:
        # Create default profile
        user = UserProfile(
            id=1,
            resume_text="Please upload your resume",
            preferences=json.dumps({}),
            target_companies=json.dumps([]),
            blacklisted_companies=json.dumps([])
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    
    return user.to_dict()


@router.put("/profile")
def update_profile(
    profile_data: UserProfileUpdate,
    db: Session = Depends(get_db)
):
    """Update user profile"""
    user = db.query(UserProfile).filter(UserProfile.id == 1).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    # Update fields
    update_dict = profile_data.dict(exclude_unset=True)
    
    # Handle search_keywords - append instead of replace
    if 'search_keywords' in update_dict and update_dict['search_keywords']:
        new_keywords = update_dict['search_keywords']
        existing_keywords = user.search_keywords or ""
        
        if existing_keywords:
            # Combine existing and new keywords, remove duplicates
            existing_set = {k.strip().lower() for k in existing_keywords.split(',')}
            new_list = [k.strip() for k in new_keywords.split(',') if k.strip()]
            
            # Add only new keywords that don't exist
            for keyword in new_list:
                if keyword.lower() not in existing_set:
                    existing_keywords += f", {keyword}"
            
            update_dict['search_keywords'] = existing_keywords
            logger.info(f"Appended keywords. Total: {len(existing_keywords.split(','))}")
        else:
            update_dict['search_keywords'] = new_keywords
            logger.info(f"Set initial keywords: {new_keywords}")
    
    # Handle JSON fields
    if 'preferences' in update_dict:
        update_dict['preferences'] = json.dumps(update_dict['preferences'])
    if 'target_companies' in update_dict:
        update_dict['target_companies'] = json.dumps(update_dict['target_companies'])
    if 'blacklisted_companies' in update_dict:
        update_dict['blacklisted_companies'] = json.dumps(update_dict['blacklisted_companies'])
    
    for key, value in update_dict.items():
        setattr(user, key, value)
    
    user.updated_at = datetime.now()
    db.commit()
    db.refresh(user)
    
    logger.info("User profile updated")
    
    return {"message": "Profile updated successfully", "profile": user.to_dict()}


@router.post("/resume")
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload and parse resume (PDF or DOCX)"""
    
    # Validate file type
    allowed_extensions = ['.pdf', '.docx', '.txt']
    file_ext = os.path.splitext(file.filename)[1].lower()
    
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed: {', '.join(allowed_extensions)}"
        )
    
    # Save file
    os.makedirs("data/resumes", exist_ok=True)
    file_path = f"data/resumes/resume_{datetime.now().strftime('%Y%m%d_%H%M%S')}{file_ext}"
    
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    
    logger.info(f"Resume uploaded: {file_path}")
    
    # Parse resume
    parser = ResumeParser()
    parsed = parser.parse_resume(file_path)
    
    if parsed.get('error'):
        raise HTTPException(status_code=400, detail=parsed['error'])
    
    # Update user profile
    user = db.query(UserProfile).filter(UserProfile.id == 1).first()
    
    if not user:
        user = UserProfile(
            id=1,
            resume_text=parsed['text'],
            preferences=json.dumps({}),
            target_companies=json.dumps([]),
            blacklisted_companies=json.dumps([])
        )
        db.add(user)
    else:
        user.resume_text = parsed['text']
    
    if file_ext == '.pdf':
        user.resume_pdf_path = file_path
    elif file_ext == '.docx':
        user.resume_docx_path = file_path
    
    user.years_experience = parsed.get('experience_years', 0)
    user.updated_at = datetime.now()
    
    db.commit()
    
    return {
        "message": "Resume uploaded and parsed successfully",
        "file_path": file_path,
        "skills_found": parsed.get('skills', []),
        "experience_years": parsed.get('experience_years', 0)
    }


@router.get("/resumes")
def list_resume_versions(db: Session = Depends(get_db)):
    """List all resume versions"""
    versions = db.query(ResumeVersion).order_by(ResumeVersion.created_at.desc()).all()
    return {"versions": [v.to_dict() for v in versions]}


@router.post("/resumes")
def create_resume_version(
    version_name: str,
    resume_text: str,
    focus_keywords: Optional[list] = None,
    target_roles: Optional[list] = None,
    db: Session = Depends(get_db)
):
    """Create new resume version"""
    version = ResumeVersion(
        version_name=version_name,
        resume_text=resume_text,
        focus_keywords=json.dumps(focus_keywords or []),
        target_roles=json.dumps(target_roles or [])
    )
    db.add(version)
    db.commit()
    db.refresh(version)
    
    return {"message": "Resume version created", "version": version.to_dict()}


@router.get("/cover-letters")
def list_cover_letter_templates(db: Session = Depends(get_db)):
    """List all cover letter templates"""
    templates = db.query(CoverLetterTemplate).order_by(CoverLetterTemplate.created_at.desc()).all()
    return {"templates": [t.to_dict() for t in templates]}


@router.post("/cover-letters")
def create_cover_letter_template(
    template_name: str,
    content: str,
    placeholders: Optional[dict] = None,
    db: Session = Depends(get_db)
):
    """Create new cover letter template"""
    template = CoverLetterTemplate(
        template_name=template_name,
        content=content,
        placeholders=json.dumps(placeholders or {})
    )
    db.add(template)
    db.commit()
    db.refresh(template)
    
    return {"message": "Cover letter template created", "template": template.to_dict()}


@router.put("/preferences")
def update_preferences(
    keywords: Optional[list] = None,
    locations: Optional[list] = None,
    salary_min: Optional[int] = None,
    job_types: Optional[list] = None,
    db: Session = Depends(get_db)
):
    """Update search preferences"""
    user = db.query(UserProfile).filter(UserProfile.id == 1).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    # Get current preferences
    prefs = json.loads(user.preferences) if user.preferences else {}
    
    # Update preferences
    if keywords is not None:
        prefs['keywords'] = keywords
    if locations is not None:
        prefs['locations'] = locations
    if salary_min is not None:
        prefs['salary_min'] = salary_min
    if job_types is not None:
        prefs['job_types'] = job_types
    
    user.preferences = json.dumps(prefs)
    user.updated_at = datetime.now()
    db.commit()
    
    return {"message": "Preferences updated", "preferences": prefs}
