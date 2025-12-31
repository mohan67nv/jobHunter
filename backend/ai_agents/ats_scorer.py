"""
ATS Scorer Agent
Analyzes resume for Applicant Tracking System compatibility
"""
from typing import Dict, List
from ai_agents.base_agent import BaseAgent
from ai_agents.model_config import get_model_config


class ATSScorer(BaseAgent):
    """Scores resume for ATS compatibility"""
    
    def __init__(self):
        config = get_model_config("ATSScorer")
        super().__init__(preferred_provider=config["provider"], model=config["model"])
    
    def process(self, resume_text: str, job_description: str) -> Dict:
        """
        Analyze resume for ATS compatibility
        
        Args:
            resume_text: Full resume text
            job_description: Job description text
            
        Returns:
            Dictionary with ATS analysis
        """
        prompt = f"""
Analyze this resume for ATS (Applicant Tracking System) compatibility against the job description. Return ONLY valid JSON:

{{
    "ats_score": 92,
    "keyword_match": 78,
    "keyword_details": {{
        "total_jd_keywords": 45,
        "found_in_resume": 35,
        "missing_keywords": ["keyword1", "keyword2"]
    }},
    "formatting_score": 95,
    "formatting_issues": ["Issue 1", "Issue 2"],
    "section_structure_score": 90,
    "missing_sections": ["Publications"],
    "recommendations": [
        "Add 'Machine Learning' keyword in skills section",
        "Use standard section headers",
        "Include keywords naturally in experience descriptions"
    ],
    "critical_issues": [],
    "strengths": ["Clear section headers", "Good keyword density", "Proper date formatting"]
}}

Job Description:
{job_description[:2000]}

Resume:
{resume_text[:3000]}

Scoring criteria:
- keyword_match: Percentage of JD keywords found in resume (0-100)
- formatting_score: Resume format quality (0-100)
- section_structure_score: Section organization quality (0-100)
- ats_score: Overall ATS compatibility (weighted average)

Identify specific issues and provide actionable recommendations.
"""
        
        response = self.generate(prompt, temperature=0.3)
        
        if not response:
            return self._get_default_ats_score()
        
        parsed = self.parse_json_response(response)
        
        if not parsed:
            return self._get_default_ats_score()
        
        # Normalize data
        ats_data = self._normalize_ats_score(parsed)
        
        return ats_data
    
    def _normalize_ats_score(self, data: Dict) -> Dict:
        """Ensure ATS score data has all required fields"""
        # Validate scores are in range
        ats_score = max(0, min(100, data.get('ats_score', 0)))
        keyword_match = max(0, min(100, data.get('keyword_match', 0)))
        formatting_score = max(0, min(100, data.get('formatting_score', 0)))
        section_structure_score = max(0, min(100, data.get('section_structure_score', 0)))
        
        return {
            'ats_score': ats_score,
            'keyword_match': keyword_match,
            'keyword_details': data.get('keyword_details', {
                'total_jd_keywords': 0,
                'found_in_resume': 0,
                'missing_keywords': []
            }),
            'formatting_score': formatting_score,
            'formatting_issues': data.get('formatting_issues', []),
            'section_structure_score': section_structure_score,
            'missing_sections': data.get('missing_sections', []),
            'recommendations': data.get('recommendations', []),
            'critical_issues': data.get('critical_issues', []),
            'strengths': data.get('strengths', []),
        }
    
    def _get_default_ats_score(self) -> Dict:
        """Return default ATS score when AI fails"""
        return {
            'ats_score': 70,
            'keyword_match': 0,
            'keyword_details': {
                'total_jd_keywords': 0,
                'found_in_resume': 0,
                'missing_keywords': []
            },
            'formatting_score': 0,
            'formatting_issues': [],
            'section_structure_score': 0,
            'missing_sections': [],
            'recommendations': ['AI analysis unavailable - manual review recommended'],
            'critical_issues': [],
            'strengths': [],
        }
