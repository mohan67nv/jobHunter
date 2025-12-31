"""
AI analysis endpoints - Enhanced with industry-standard ATS scoring
"""
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from database import get_db
from models.job import Job, JobAnalysis
from models.user import UserProfile
from schemas.analysis import AnalysisRequest, AnalysisResponse
from ai_agents.agent_manager import AgentManager
from ai_agents.enhanced_ats_scorer import EnhancedATSScorer
from utils.logger import setup_logger

router = APIRouter(prefix="/api/analysis", tags=["analysis"])
logger = setup_logger(__name__)


class CustomCompareRequest(BaseModel):
    resume_text: str
    job_description: str


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
    """
    Get comprehensive interview preparation materials with Q&A
    Includes: Company Info, Technical Q&A (with Glassdoor insights), Behavioral Q&A, HR Q&A
    """
    job = db.query(Job).get(job_id)
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Get user's resume for personalized project questions
    user = db.query(UserProfile).filter(UserProfile.id == 1).first()
    resume_text = user.resume_text if user else None
    
    # Use CompanyResearcher with GPT-4o-mini for comprehensive interview prep
    from ai_agents.researcher import CompanyResearcher
    
    try:
        researcher = CompanyResearcher(preferred_provider="openai")
        result = researcher.process(
            company_name=job.company,
            job_title=job.title,
            job_description=job.description,
            resume_text=resume_text
        )
        
        return {
            "job_id": job_id,
            "job_title": job.title,
            "company": job.company,
            "company_info": result.get('company_info', {}),
            "technical_qa": result.get('technical_qa', []),
            "behavioral_qa": result.get('behavioral_qa', []),
            "hr_qa": result.get('hr_qa', [])
        }
    except Exception as e:
        logger.error(f"Error generating interview prep for job {job_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate interview prep: {str(e)}")


@router.post("/enhanced-ats-scan/{job_id}")
def enhanced_ats_scan(
    job_id: int, 
    use_multi_layer: bool = False,
    tier: str = 'standard',
    db: Session = Depends(get_db)
):
    """
    Industry-standard ATS scan (JobScan level)
    
    Args:
        job_id: Job to analyze
        use_multi_layer: Enable 3-layer AI scoring (DeepSeek + GPT-5-mini)
        tier: 'basic' (score only), 'standard' (score + insights), 'premium' (full feedback)
    
    Returns:
        Legacy mode: Keywords, Font, Layout, Page Setup (30+ checks)
        Multi-layer mode: 3-layer AI score with tier-based feedback
    """
    job = db.query(Job).get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Get user profile
    user = db.query(UserProfile).filter(UserProfile.id == 1).first()
    if not user or not user.resume_text:
        raise HTTPException(status_code=400, detail="No resume found. Upload resume in Profile first.")
    
    # Run enhanced ATS analysis
    try:
        ats_scorer = EnhancedATSScorer(use_multi_layer=use_multi_layer)
        result = ats_scorer.process(user.resume_text, job.description, tier=tier)
        
        response = {
            "job_id": job_id,
            "job_title": job.title,
            "company": job.company,
            "scoring_mode": "multi_layer" if use_multi_layer else "legacy",
            "tier": tier if use_multi_layer else "legacy"
        }
        
        if use_multi_layer:
            # Multi-layer response format
            response.update({
                "final_score": result['final_score'],
                "confidence": result['confidence'],
                "layer_scores": result['layer_scores'],
                "detailed_feedback": result.get('detailed_feedback'),
                "cost_breakdown": result.get('cost_breakdown'),
                "processing_time": result.get('processing_time')
            })
        else:
            # Legacy response format
            response.update({
                "ats_score": result['ats_score'],
                "keyword_analysis": result['keyword_analysis'],
                "font_check": result['font_check'],
                "layout_check": result['layout_check'],
                "page_setup_check": result['page_setup_check'],
                "structure_analysis": result['structure_analysis'],
                "overall_recommendations": result['overall_recommendations']
            })
        
        return response
    except Exception as e:
        logger.error(f"Enhanced ATS scan failed: {e}")
        raise HTTPException(status_code=500, detail=f"ATS scan failed: {str(e)}")


@router.post("/compare-custom")
def compare_custom_cv_jd(
    request: CustomCompareRequest,
    db: Session = Depends(get_db)
):
    """
    Compare custom CV text with job description (without saving to database)
    
    - **resume_text**: Your resume/CV text
    - **job_description**: Job description to compare against
    
    Returns match analysis with score, matching skills, gaps, and recommendations
    """
    try:
        from ai_agents.jd_analyzer import JDAnalyzer
        from ai_agents.matcher import ResumeMatcher
        
        if not request.resume_text or not request.resume_text.strip():
            raise HTTPException(status_code=400, detail="Resume text is required")
        
        if not request.job_description or not request.job_description.strip():
            raise HTTPException(status_code=400, detail="Job description is required")
        
        logger.info("🔍 Analyzing custom CV-JD comparison...")
        
        # Step 1: Analyze job description
        jd_analyzer = JDAnalyzer()
        jd_analysis = jd_analyzer.process(request.job_description)
        
        # Step 2: Match resume to job
        matcher = ResumeMatcher()
        match_result = matcher.process(request.resume_text, request.job_description, jd_analysis)
        
        # Step 3: Calculate ATS score
        ats_scorer = EnhancedATSScorer()
        ats_result = ats_scorer.process(request.resume_text, request.job_description)
        
        logger.info(f"✅ Custom comparison complete: Match {match_result['match_score']}%, ATS {ats_result['ats_score']}%")
        
        return {
            "match_score": match_result['match_score'],
            "ats_score": ats_result['ats_score'],
            "keyword_density": ats_result.get('keyword_analysis', {}).get('keyword_match_rate', 0),
            "matching_skills": match_result['matching_skills'],
            "missing_skills": match_result['missing_skills'],
            "experience_match": match_result['experience_match'],
            "education_match": match_result['education_match'],
            "strengths": match_result['strengths'],
            "concerns": match_result['concerns'],
            "overall_assessment": match_result['overall_assessment'],
            "ats_details": {
                "keyword_analysis": ats_result.get('keyword_analysis', {}),
                "font_check": ats_result.get('font_check', {}),
                "layout_check": ats_result.get('layout_check', {}),
                "structure_analysis": ats_result.get('structure_analysis', {}),
                "recommendations": ats_result.get('overall_recommendations', [])
            },
            "job_requirements": {
                "required_skills": jd_analysis.get('required_skills', []),
                "nice_to_have": jd_analysis.get('nice_to_have', []),
                "experience_years": jd_analysis.get('experience_years', 0),
                "education": jd_analysis.get('education_required', 'Not specified')
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Custom CV-JD comparison failed: {e}")
        raise HTTPException(status_code=500, detail=f"Comparison failed: {str(e)}")
