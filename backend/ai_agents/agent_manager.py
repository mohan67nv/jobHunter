"""
Agent Manager - orchestrates all AI agents for complete job analysis
"""
from typing import Dict, Optional
import json
from datetime import datetime
from sqlalchemy.orm import Session
from models.job import Job, JobAnalysis
from models.user import UserProfile
from ai_agents.jd_analyzer import JDAnalyzer
from ai_agents.matcher import ResumeMatcher
from ai_agents.enhanced_ats_scorer import EnhancedATSScorer
from ai_agents.optimizer import ApplicationOptimizer
from ai_agents.researcher import CompanyResearcher
from utils.logger import setup_logger

logger = setup_logger(__name__)


class AgentManager:
    """Manages and orchestrates all AI agents for job analysis"""
    
    def __init__(self, db: Session, preferred_provider: str = "openai"):
        """
        Initialize AgentManager
        
        Args:
            db: Database session
            preferred_provider: Preferred AI provider (models selected from model_config.py)
        """
        self.db = db
        
        # Initialize all agents - each uses optimal model from model_config.py
        self.analyzer = JDAnalyzer()              # DeepSeek Coder - fast parsing
        self.matcher = ResumeMatcher()            # DeepSeek Chat - matching
        self.ats_scorer = EnhancedATSScorer(use_multi_layer=True)  # 3-layer AI scoring
        self.optimizer = ApplicationOptimizer()   # DeepSeek Coder - optimization
        self.researcher = CompanyResearcher()     # GPT-5-mini - research
        
        logger.info("✅ AgentManager initialized with multi-layer ATS scoring")
    
    def analyze_job(self, job_id: int, generate_materials: bool = True) -> Optional[JobAnalysis]:
        """
        Run complete AI analysis on job
        
        Args:
            job_id: ID of job to analyze
            generate_materials: Whether to generate tailored resume/cover letter
            
        Returns:
            JobAnalysis object or None if failed
        """
        logger.info(f"🤖 Running AI analysis on job {job_id}...")
        
        # Get job from database
        job = self.db.query(Job).get(job_id)
        if not job:
            logger.error(f"Job {job_id} not found")
            return None
        
        # Get user profile
        user = self.db.query(UserProfile).filter(UserProfile.id == 1).first()
        if not user or not user.resume_text:
            logger.error("User profile or resume not found")
            return None
        
        try:
            # Step 1: Analyze Job Description
            logger.info("  1/5: Analyzing job description...")
            jd_analysis = self.jd_analyzer.process(job.description)
            
            # Step 2: Match Resume to Job
            logger.info("  2/5: Matching resume to job...")
            match_analysis = self.matcher.process(
                user.resume_text,
                job.description,
                jd_analysis
            )
            
            # Step 3: Calculate ATS Score (Multi-Layer: DeepSeek + GPT-5-mini + DeepSeek Reasoner)
            logger.info("  3/5: Running 3-layer ATS scoring (this may take 10-15 seconds)...")
            ats_analysis = self.ats_scorer.process(
                user.resume_text,
                job.description,
                tier='premium'  # Always use full feedback
            )
            logger.info(f"     ✓ ATS Score: {ats_analysis.get('final_score', ats_analysis.get('ats_score', 0))}")
            
            # Step 4: Generate Optimized Materials
            tailored_resume = None
            tailored_cover_letter = None
            
            if generate_materials:
                logger.info("  4/5: Generating tailored materials...")
                job_data = {
                    'title': job.title,
                    'company': job.company,
                    'description': job.description
                }
                
                optimized = self.optimizer.process(
                    user.resume_text,
                    job_data,
                    match_analysis,
                    user_info=user.to_dict(),
                    generate_type="both"
                )
                
                tailored_resume = optimized.get('tailored_resume')
                tailored_cover_letter = optimized.get('tailored_cover_letter')
            else:
                logger.info("  4/5: Skipping material generation")
            
            # Step 5: Research Company and Generate Interview Questions
            logger.info("  5/5: Researching company...")
            company_research = self.researcher.process(
                job.company,
                job.title,
                job.description
            )
            
            interview_questions = company_research.get('likely_questions', [])
            
            # Combine all analyses
            combined_analysis = self._combine_analyses(
                match_analysis,
                ats_analysis,
                jd_analysis,
                tailored_resume,
                tailored_cover_letter,
                interview_questions
            )
            
            # Save to database
            analysis = self._save_analysis(job_id, combined_analysis)
            
            logger.info(f"✅ Analysis complete: Match {combined_analysis['match_score']:.0f}%, ATS {combined_analysis['ats_score']:.0f}%")
            
            return analysis
        
        except Exception as e:
            logger.error(f"❌ Error analyzing job {job_id}: {e}")
            return None
    
    def _combine_analyses(self, match_analysis: Dict, ats_analysis: Dict,
                         jd_analysis: Dict, tailored_resume: Optional[str],
                         tailored_cover_letter: Optional[str],
                         interview_questions: list) -> Dict:
        """Combine all analysis results into single structure"""
        
        # Extract ATS score (support both multi-layer and legacy format)
        if isinstance(ats_analysis, dict):
            # Multi-layer format has 'final_score', legacy has 'ats_score'
            ats_score = ats_analysis.get('final_score', ats_analysis.get('ats_score', 70))
        else:
            ats_score = 70  # Fallback
        
        # Extract matching skills from match analysis
        matching_skills = [s['skill'] for s in match_analysis.get('matching_skills', [])]
        
        # Extract missing keywords and detailed feedback from ATS analysis
        missing_keywords = []
        ats_recommendations = []
        
        # Multi-layer ATS format
        if 'detailed_feedback' in ats_analysis and ats_analysis['detailed_feedback']:
            feedback = ats_analysis['detailed_feedback']
            
            # Extract immediate fixes
            if 'immediate_fixes' in feedback:
                for fix in feedback.get('immediate_fixes', [])[:3]:
                    if isinstance(fix, dict):
                        ats_recommendations.append(f"🎯 {fix.get('action', '')} (Impact: {fix.get('impact', '')})") 
            
            # Extract strategic improvements
            if 'strategic_improvements' in feedback:
                for improvement in feedback.get('strategic_improvements', [])[:2]:
                    if isinstance(improvement, dict):
                        ats_recommendations.append(f"📈 {improvement.get('action', '')}")
            
            # Extract overall recommendation
            if 'overall_recommendation' in feedback:
                ats_recommendations.insert(0, f"💡 {feedback['overall_recommendation']}")
        
        # Legacy format fallback
        if 'keyword_analysis' in ats_analysis:
            missing_keywords = ats_analysis['keyword_analysis'].get('missing_critical_keywords', [])
        
        # If no detailed feedback, use basic recommendations
        if not ats_recommendations:
            ats_recommendations = ats_analysis.get('recommendations', [
                "Optimize resume keywords to match job description",
                "Quantify achievements with specific metrics",
                "Use ATS-friendly formatting"
            ])
        
        # Calculate keyword density
        keyword_density = 0
        if 'keyword_analysis' in ats_analysis:
            keyword_density = ats_analysis['keyword_analysis'].get('keyword_density', 0)
        keyword_match = ats_analysis.get('keyword_match', 0)
        keyword_density = keyword_match  # Simplified
        
        # Combine recommendations with detailed feedback from multi-layer ATS
        recommendations = {
            'resume': ats_recommendations,  # Now includes detailed feedback from DeepSeek Reasoner
            'cover_letter': [
                f"Emphasize: {', '.join(matching_skills[:3])}" if matching_skills else "Highlight relevant skills",
                "Include specific achievements with metrics",
                "Show enthusiasm for company and role"
            ],
            'interview': [
                "Prepare STAR method examples for key achievements",
                "Research company recent news and developments",
                "Practice technical questions based on job requirements"
            ]
        }
        
        # Determine experience match level
        experience_match = match_analysis.get('experience_match', 'Unknown')
        if 'perfect' in experience_match.lower() or 'exceeds' in experience_match.lower():
            exp_match_level = "Perfect"
        elif 'close' in experience_match.lower():
            exp_match_level = "Close"
        else:
            exp_match_level = "Gap"
        
        # Determine salary match (simplified - would need actual salary data)
        salary_match = "Unknown"
        
        return {
            'match_score': match_analysis.get('match_score', 0),
            'ats_score': ats_score,  # Now from multi-layer scoring (30% + 40% + 30%)
            'matching_skills': json.dumps(matching_skills),
            'missing_skills': json.dumps(match_analysis.get('missing_skills', [])),
            'experience_match': exp_match_level,
            'salary_match': salary_match,
            'keyword_density': keyword_density,
            'recommendations': json.dumps(recommendations),  # Includes DeepSeek Reasoner feedback
            'tailored_resume': tailored_resume,
            'tailored_cover_letter': tailored_cover_letter,
            'interview_questions': json.dumps(interview_questions),
        }
    
    def _save_analysis(self, job_id: int, analysis_data: Dict) -> JobAnalysis:
        """Save analysis to database"""
        try:
            # Check if analysis already exists
            existing = self.db.query(JobAnalysis).filter(JobAnalysis.job_id == job_id).first()
            
            if existing:
                # Update existing
                for key, value in analysis_data.items():
                    if hasattr(existing, key):
                        setattr(existing, key, value)
                existing.analyzed_at = datetime.now()
                analysis = existing
            else:
                # Create new
                analysis = JobAnalysis(
                    job_id=job_id,
                    **analysis_data
                )
                self.db.add(analysis)
            
            self.db.commit()
            self.db.refresh(analysis)
            
            return analysis
        
        except Exception as e:
            logger.error(f"Error saving analysis: {e}")
            self.db.rollback()
            raise
    
    def batch_analyze(self, job_ids: list, max_concurrent: int = 5) -> Dict:
        """
        Analyze multiple jobs (with rate limiting)
        
        Args:
            job_ids: List of job IDs to analyze
            max_concurrent: Maximum concurrent analyses
            
        Returns:
            Dictionary with statistics
        """
        logger.info(f"📊 Batch analyzing {len(job_ids)} jobs...")
        
        stats = {
            'total': len(job_ids),
            'success': 0,
            'failed': 0,
            'errors': []
        }
        
        for job_id in job_ids:
            try:
                result = self.analyze_job(job_id, generate_materials=False)
                if result:
                    stats['success'] += 1
                else:
                    stats['failed'] += 1
            except Exception as e:
                stats['failed'] += 1
                stats['errors'].append({'job_id': job_id, 'error': str(e)})
                logger.error(f"Error analyzing job {job_id}: {e}")
        
        logger.info(f"✅ Batch analysis complete: {stats['success']} success, {stats['failed']} failed")
        
        return stats
    
    def get_analysis(self, job_id: int) -> Optional[Dict]:
        """
        Get analysis for job (run if doesn't exist)
        
        Args:
            job_id: Job ID
            
        Returns:
            Analysis dictionary or None
        """
        analysis = self.db.query(JobAnalysis).filter(JobAnalysis.job_id == job_id).first()
        
        if not analysis:
            # Run analysis if not exists
            analysis = self.analyze_job(job_id)
        
        return analysis.to_dict() if analysis else None
