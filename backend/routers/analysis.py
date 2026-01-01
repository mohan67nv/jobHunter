"""
AI analysis endpoints - Enhanced with industry-standard ATS scoring
"""
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from database import get_db
from models.job import Job, JobAnalysis
from models.user import UserProfile
from schemas.analysis import AnalysisRequest, AnalysisResponse
from ai_agents.agent_manager import AgentManager
from ai_agents.enhanced_ats_scorer import EnhancedATSScorer
from ai_agents.multi_layer_ats import MultiLayerATSScorer
from utils.logger import setup_logger
from utils.pdf_parser import PDFParser

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
    Run full AI analysis on job with multi-layer ATS scoring
    
    - **job_id**: ID of job to analyze
    - **generate_materials**: Whether to generate tailored resume/cover letter
    
    Analysis includes:
    1. Job description parsing (DeepSeek Coder)
    2. Resume-JD matching (DeepSeek Chat)
    3. 3-layer ATS scoring (DeepSeek + GPT-5-mini + DeepSeek Reasoner)
    4. Tailored materials generation (optional)
    5. Company research & interview prep (GPT-5-mini)
    
    Expected time: 20-40 seconds for complete analysis
    """
    job = db.query(Job).get(job_id)
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Check user profile exists
    user = db.query(UserProfile).filter(UserProfile.id == 1).first()
    if not user or not user.resume_text:
        raise HTTPException(status_code=400, detail="No resume found. Upload resume in Profile first.")
    
    # Run analysis in background
    def run_analysis():
        try:
            agent_manager = AgentManager(db)
            result = agent_manager.analyze_job(job_id, generate_materials)
            if result:
                logger.info(f"✅ Analysis completed successfully for job {job_id}")
            else:
                logger.error(f"❌ Analysis failed for job {job_id}")
        except Exception as e:
            logger.error(f"❌ Error in background analysis for job {job_id}: {e}")
    
    background_tasks.add_task(run_analysis)
    
    return {
        "message": "AI analysis started (3-layer ATS with detailed feedback)",
        "job_id": job_id,
        "estimated_time": "20-40 seconds",
        "steps": [
            "1. Analyzing job description",
            "2. Matching resume to job",
            "3. Running 3-layer ATS scoring",
            "4. Generating tailored materials" if generate_materials else "4. Skipping materials",
            "5. Researching company"
        ]
    }


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
    🎯 COMPREHENSIVE ATS Keyword Analysis - Industry-Leading CV-JD Comparison
    
    - **resume_text**: Your resume/CV text
    - **job_description**: Job description to compare against
    
    🔥 What makes this better than competitors:
    
    1. **Deep JD Analysis with DeepSeek Reasoner**:
       - Extracts ALL ATS-critical keywords (technical, leadership, soft skills)
       - Categorizes by importance (0-100 score)
       - Identifies implicit requirements (e.g., "oversee" = needs leadership keywords)
       - Finds reference numbers, company-specific terms
    
    2. **3-Layer ATS Scoring**:
       - Layer 1: DeepSeek-V3.2 (30%) - Fast baseline
       - Layer 2: GPT-5-mini (40%) - Validation (highest weight)
       - Layer 3: DeepSeek-R1 (30%) - Deep reasoning
    
    3. **Strategic Gap Analysis**:
       - Missing critical keywords with exact recommendations
       - Under-emphasized keywords (found but not enough)
       - Section-by-section improvement guide
       - Estimated ATS score after fixes
    
    4. **Visual Comparison Table**:
       - Side-by-side JD requirements vs Resume status
       - Priority actions ranked by impact
       - Exact text replacements suggested
    
    Returns comprehensive analysis matching top industry tools (JobScan level)
    """
    try:
        from ai_agents.jd_analyzer import JDAnalyzer
        from ai_agents.matcher import ResumeMatcher
        from ai_agents.ats_keyword_analyzer import ATSKeywordAnalyzer
        from ai_agents.resume_optimizer import ResumeOptimizer
        import time
        
        if not request.resume_text or not request.resume_text.strip():
            raise HTTPException(status_code=400, detail="Resume text is required")
        
        if not request.job_description or not request.job_description.strip():
            raise HTTPException(status_code=400, detail="Job description is required")
        
        start_time = time.time()
        logger.info("🔍 Starting COMPREHENSIVE ATS Keyword Analysis with DeepSeek Reasoner...")
        
        # Step 1: Deep JD keyword extraction with DeepSeek Reasoner
        logger.info("📊 Step 1/7: Deep JD analysis with DeepSeek Reasoner...")
        keyword_analyzer = ATSKeywordAnalyzer()
        jd_keywords = keyword_analyzer.analyze_jd_keywords(request.job_description)
        
        # Step 2: Analyze job description (for skills/requirements)
        logger.info("📋 Step 2/7: Analyzing job requirements...")
        jd_analyzer = JDAnalyzer()
        jd_analysis = jd_analyzer.process(request.job_description)
        
        # Step 3: Match resume to job (for compatibility score)
        logger.info("🎯 Step 3/7: Calculating resume-job match score...")
        matcher = ResumeMatcher()
        match_result = matcher.process(request.resume_text, request.job_description, jd_analysis)
        
        # Step 4: Anonymize resume before sending to LLMs (security)
        logger.info("🔒 Step 4/7: Anonymizing resume (removing PII)...")
        from utils.anonymizer import get_anonymizer
        anonymizer = get_anonymizer()
        anon_result = anonymizer.anonymize(request.resume_text)
        anonymized_resume = anon_result['anonymized_text']
        logger.info(f"   ✅ Removed {len(anon_result['removed_pii'])} PII items for security")
        
        # Step 5: Strategic gap analysis with recommendations (THIS GIVES REALISTIC ATS SCORE)
        logger.info("💡 Step 5/7: Analyzing keyword gaps and generating recommendations...")
        gap_analysis = keyword_analyzer.analyze_cv_gaps(request.resume_text, jd_keywords)
        
        # USE GAP ANALYSIS SCORE AS THE MAIN ATS SCORE (more realistic than multi-layer)
        realistic_ats_score = gap_analysis.get('current_ats_score', 0)
        estimated_after_fixes = gap_analysis.get('estimated_score_after_fixes', 0)
        
        logger.info(f"   🎯 Realistic ATS Score: {realistic_ats_score}% (from deep keyword analysis)")
        
        # Step 6: Multi-Layer ATS Scoring (for detailed breakdown only - not primary score)
        logger.info("🏆 Step 6/7: Running 3-layer ATS for detailed breakdown...")
        multi_layer_scorer = MultiLayerATSScorer()
        ats_result = multi_layer_scorer.assess_resume(anonymized_resume, request.job_description)
        
        # Step 7: Advanced Resume Optimization (JD-specific summary, experience bullets, skills)
        logger.info("✨ Step 7/7: Generating advanced resume optimizations...")
        resume_optimizer = ResumeOptimizer()
        optimization = resume_optimizer.process(
            request.resume_text,
            request.job_description,
            gap_analysis.get('missing_critical', [])[:10]
        )
        
        # Step 8: Generate visual comparison table
        logger.info("📊 Building visual comparison table...")
        comparison_table = keyword_analyzer.generate_comparison_table(jd_keywords, gap_analysis)
        
        elapsed = time.time() - start_time
        
        logger.info(f"✅ COMPREHENSIVE ANALYSIS COMPLETE in {elapsed:.1f}s")
        logger.info(f"   Match: {match_result['match_score']}% | Realistic ATS: {realistic_ats_score}%")
        logger.info(f"   Current ATS: {realistic_ats_score}% → After fixes: {estimated_after_fixes}% (+{estimated_after_fixes - realistic_ats_score}%)")
        logger.info(f"   Missing critical: {len(gap_analysis.get('missing_critical', []))} | Strategic improvements: {len(gap_analysis.get('strategic_improvements', []))}")
        logger.info(f"   Advanced optimizations: Summary={bool(optimization.get('jd_specific_summary'))}, "
                   f"Experience bullets={len(optimization.get('experience_bullet_suggestions', []))}, "
                   f"Skills={len(optimization.get('skills_section_suggestions', {}).get('hard_skills_to_add', []))}")
        
        return {
            # Basic scores (USE REALISTIC ATS SCORE FROM KEYWORD ANALYSIS)
            "match_score": match_result['match_score'],
            "ats_score": realistic_ats_score,  # ← CHANGED: Use realistic score from keyword analyzer
            "keyword_density": ats_result.get('keyword_analysis', {}).get('keyword_match_rate', 0),
            
            # Multi-layer breakdown (for reference only - not primary score)
            "multi_layer_breakdown": {
                "layer1_baseline": ats_result.get('layer1_score', 0),
                "layer1_weight": "30%",
                "layer2_validation": ats_result.get('layer2_score', 0),
                "layer2_weight": "40%",
                "layer3_reasoning": ats_result.get('layer3_score', 0),
                "layer3_weight": "30%",
                "note": "Multi-layer gives optimistic score. Main ATS score above is from realistic keyword analysis."
            },
            
            # Keyword analysis (COMPREHENSIVE)
            "keyword_analysis": {
                "categorized_keywords": jd_keywords,
                "gap_analysis": gap_analysis,
                "comparison_table": comparison_table,
                "current_ats_score": realistic_ats_score,  # ← Consistent with main score
                "estimated_score_after_fixes": estimated_after_fixes,
                "score_improvement_potential": estimated_after_fixes - realistic_ats_score
            },
            
            # ADVANCED RESUME OPTIMIZATIONS
            "resume_optimizations": {
                "jd_specific_summary": optimization.get('jd_specific_summary', {}),
                "experience_bullet_suggestions": optimization.get('experience_bullet_suggestions', []),
                "skills_section_suggestions": optimization.get('skills_section_suggestions', {}),
                "cv_analysis": optimization.get('cv_analysis', {})
            },
            
            # Legacy match data
            "matching_skills": match_result['matching_skills'],
            "missing_skills": match_result['missing_skills'],
            "experience_match": match_result['experience_match'],
            "education_match": match_result['education_match'],
            "strengths": match_result['strengths'],
            "concerns": match_result['concerns'],
            "overall_assessment": match_result['overall_assessment'],
            
            # Recommendations
            "recommendations": ats_result.get('recommendations', []),
            
            # ATS details
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


@router.post("/parse-resume-pdf")
async def parse_resume_pdf(
    file: UploadFile = File(...),
):
    """
    Parse PDF resume using GPT-5-mini for intelligent text extraction
    
    - **file**: PDF file to parse
    
    Returns cleaned and structured resume text
    """
    try:
        if not file.filename.endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are supported")
        
        # Read PDF bytes
        pdf_bytes = await file.read()
        
        if len(pdf_bytes) > 10 * 1024 * 1024:  # 10MB limit
            raise HTTPException(status_code=400, detail="PDF file too large (max 10MB)")
        
        logger.info(f"📄 Parsing PDF resume: {file.filename} ({len(pdf_bytes)} bytes)")
        
        # Parse PDF with GPT-5-mini
        pdf_parser = PDFParser()
        resume_text = pdf_parser.process(pdf_bytes)
        
        if not resume_text or len(resume_text.strip()) < 50:
            raise HTTPException(status_code=400, detail="Could not extract text from PDF")
        
        logger.info(f"✅ PDF parsed successfully: {len(resume_text)} characters extracted")
        
        return {
            "resume_text": resume_text,
            "filename": file.filename,
            "size_bytes": len(pdf_bytes),
            "extracted_length": len(resume_text),
            "message": "PDF parsed successfully with GPT-5-mini"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ PDF parsing error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to parse PDF: {str(e)}")
