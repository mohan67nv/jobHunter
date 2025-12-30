"""
AI analysis endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.job import Job, JobAnalysis
from schemas.analysis import AnalysisRequest, AnalysisResponse
from ai_agents.agent_manager import AgentManager
from utils.logger import setup_logger

router = APIRouter(prefix="/api/analysis", tags=["analysis"])
logger = setup_logger(__name__)


@router.post("/analyze-job/{job_id}")
def analyze_job(
    job_id: int,
    background_tasks: BackgroundTasks,
    generate_materials: bool = True,
    db: Session = Depends(get_db)
):
    """
    Run AI analysis on job
    
    - **job_id**: ID of job to analyze
    - **generate_materials**: Whether to generate tailored resume/cover letter
    """
    job = db.query(Job).get(job_id)
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Run analysis in background
    def run_analysis():
        agent_manager = AgentManager(db)
        agent_manager.analyze_job(job_id, generate_materials)
    
    background_tasks.add_task(run_analysis)
    
    return {"message": "Analysis started", "job_id": job_id}


@router.post("/batch-analyze")
def batch_analyze_jobs(
    job_ids: List[int],
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Analyze multiple jobs in batch
    
    - **job_ids**: List of job IDs to analyze
    """
    def run_batch_analysis():
        agent_manager = AgentManager(db)
        agent_manager.batch_analyze(job_ids)
    
    background_tasks.add_task(run_batch_analysis)
    
    return {"message": f"Batch analysis started for {len(job_ids)} jobs"}


@router.get("/{job_id}", response_model=AnalysisResponse)
def get_analysis(job_id: int, db: Session = Depends(get_db)):
    """Get analysis for job"""
    analysis = db.query(JobAnalysis).filter(JobAnalysis.job_id == job_id).first()
    
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found. Run analysis first.")
    
    return analysis.to_dict()


@router.post("/generate-resume/{job_id}")
def generate_resume(job_id: int, db: Session = Depends(get_db)):
    """Generate tailored resume for job"""
    job = db.query(Job).get(job_id)
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    agent_manager = AgentManager(db)
    
    # Get or create analysis
    analysis = agent_manager.get_analysis(job_id)
    
    if not analysis or not analysis.get('tailored_resume'):
        # Generate if doesn't exist
        agent_manager.analyze_job(job_id, generate_materials=True)
        analysis = agent_manager.get_analysis(job_id)
    
    return {
        "tailored_resume": analysis.get('tailored_resume', 'Generation failed')
    }


@router.post("/generate-cover-letter/{job_id}")
def generate_cover_letter(job_id: int, db: Session = Depends(get_db)):
    """Generate tailored cover letter for job"""
    job = db.query(Job).get(job_id)
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    agent_manager = AgentManager(db)
    
    # Get or create analysis
    analysis = agent_manager.get_analysis(job_id)
    
    if not analysis or not analysis.get('tailored_cover_letter'):
        agent_manager.analyze_job(job_id, generate_materials=True)
        analysis = agent_manager.get_analysis(job_id)
    
    return {
        "tailored_cover_letter": analysis.get('tailored_cover_letter', 'Generation failed')
    }


@router.get("/interview-prep/{job_id}")
def get_interview_prep(job_id: int, db: Session = Depends(get_db)):
    """Get interview preparation materials for job"""
    analysis = db.query(JobAnalysis).filter(JobAnalysis.job_id == job_id).first()
    
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found. Run analysis first.")
    
    job = db.query(Job).get(job_id)
    
    return {
        "job_title": job.title,
        "company": job.company,
        "interview_questions": analysis.to_dict().get('interview_questions', []),
        "key_skills_to_emphasize": analysis.to_dict().get('matching_skills', []),
        "areas_to_prepare": analysis.to_dict().get('missing_skills', []),
        "recommendations": analysis.to_dict().get('recommendations', {})
    }
