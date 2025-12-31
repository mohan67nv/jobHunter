"""
Resume-Job Matcher Agent
Calculates match score and identifies skill gaps
"""
from typing import Dict, List
from ai_agents.base_agent import BaseAgent
from ai_agents.model_config import get_model_config


class ResumeMatcher(BaseAgent):
    """Matches resume to job requirements and calculates compatibility"""
    
    def __init__(self):
        config = get_model_config("ResumeMatcher")
        super().__init__(preferred_provider=config["provider"], model=config["model"])
    
    def process(self, resume_text: str, job_description: str, jd_analysis: Dict) -> Dict:
        """
        Match resume to job requirements
        
        Args:
            resume_text: Full resume text
            job_description: Job description text
            jd_analysis: Pre-analyzed JD data from JDAnalyzer
            
        Returns:
            Dictionary with match analysis
        """
        required_skills_str = ', '.join(jd_analysis.get('required_skills', []))
        nice_to_have_str = ', '.join(jd_analysis.get('nice_to_have', []))
        experience_years = jd_analysis.get('experience_years', 0)
        
        prompt = f"""
Compare this resume to the job requirements and calculate a detailed match analysis. Return ONLY valid JSON with this structure:

{{
    "match_score": 85,
    "matching_skills": [
        {{"skill": "Python", "level": "Expert", "jd_required": "Advanced"}},
        {{"skill": "SQL", "level": "Advanced", "jd_required": "Intermediate"}}
    ],
    "missing_skills": ["Kubernetes", "MLOps"],
    "experience_match": "Perfect (5 years required, 6 years experience)",
    "education_match": "Exceeds requirements",
    "strengths": ["Exceeds ML requirements", "Perfect degree match", "Strong project portfolio"],
    "concerns": ["No Kubernetes experience mentioned", "Limited cloud experience"],
    "overall_assessment": "Strong candidate with excellent technical skills"
}}

Job Requirements:
- Required Skills: {required_skills_str}
- Nice to Have: {nice_to_have_str}
- Experience: {experience_years} years
- Education: {jd_analysis.get('education_required', 'Not specified')}

Resume:
{resume_text[:3000]}

Calculate match_score (0-100) based on:
- 40% skills match
- 30% experience match
- 20% education match
- 10% overall fit

Be realistic and thorough. Identify ALL matching and missing skills.
"""
        
        response = self.generate(prompt, temperature=0.4)
        
        if not response:
            return self._get_default_match()
        
        parsed = self.parse_json_response(response)
        
        if not parsed:
            return self._get_default_match()
        
        # Normalize and validate
        match_data = self._normalize_match(parsed)
        
        return match_data
    
    def _normalize_match(self, data: Dict) -> Dict:
        """Ensure match data has all required fields"""
        # Ensure match_score is in valid range
        match_score = data.get('match_score', 0)
        match_score = max(0, min(100, match_score))
        
        return {
            'match_score': match_score,
            'matching_skills': data.get('matching_skills', []),
            'missing_skills': data.get('missing_skills', []),
            'experience_match': data.get('experience_match', 'Unknown'),
            'education_match': data.get('education_match', 'Unknown'),
            'strengths': data.get('strengths', []),
            'concerns': data.get('concerns', []),
            'overall_assessment': data.get('overall_assessment', ''),
        }
    
    def _get_default_match(self) -> Dict:
        """Return default match structure when AI fails"""
        return {
            'match_score': 50,
            'matching_skills': [],
            'missing_skills': [],
            'experience_match': 'Unknown',
            'education_match': 'Unknown',
            'strengths': [],
            'concerns': [],
            'overall_assessment': 'Unable to analyze'
        }
    
    def analyze_job_fit(self, job, user_profile) -> Dict:
        """
        Quick match score calculation using resume + keywords
        
        Args:
            job: Job object with description, title, requirements
            user_profile: UserProfile with resume_text and search_keywords
            
        Returns:
            Dict with match_score and matched/missing skills
        """
        # Get user data
        resume_text = user_profile.resume_text or ""
        keywords = user_profile.search_keywords or ""
        
        # Get job data
        job_title = job.title
        job_desc = job.description or ""
        job_reqs = job.requirements or ""
        
        # Combine user profile data
        user_profile_text = f"Resume: {resume_text[:2000]}\n\nTarget Keywords: {keywords}"
        job_text = f"Title: {job_title}\n\nDescription: {job_desc[:1500]}\n\nRequirements: {job_reqs[:500]}"
        
        prompt = f"""Calculate job match score. Return ONLY valid JSON:

{{
    "match_score": 75,
    "skills_matched": ["Python", "PyTorch", "TensorFlow", "Scikit-learn", "NumPy", "Pandas", "Docker", "Kubernetes"],
    "skills_missing": ["AWS", "React"],
    "summary": "Strong match with 75% compatibility",
    "recommendations": "Consider learning AWS and React"
}}

User Profile:
{user_profile_text}

Job Posting:
{job_text}

Scoring Instructions:
- 50% skills match: Extract ALL technical skills from the resume (frameworks, languages, tools, platforms)
- 30% keyword relevance: Match user's target job titles/keywords against job title and description
- 20% overall fit: Experience level, domain expertise, seniority match

IMPORTANT for skills_matched:
- Include ALL skills from resume that match the job (not just 5-10)
- Consider: Programming languages, frameworks, libraries, cloud platforms, tools, methodologies
- Example: Python, PyTorch, TensorFlow, Scikit-learn, NumPy, Pandas, Azure, Docker, Kubernetes, Git, Flask, etc.

Be realistic. Score 0-100."""
        
        response = self.generate(prompt, temperature=0.3)
        
        if not response:
            return self._get_default_quick_match()
        
        parsed = self.parse_json_response(response)
        
        if not parsed:
            return self._get_default_quick_match()
        
        # Normalize
        match_score = parsed.get('match_score', 50)
        match_score = max(0, min(100, match_score))
        
        return {
            'match_score': match_score,
            'skills_matched': parsed.get('skills_matched', []),
            'skills_missing': parsed.get('skills_missing', []),
            'summary': parsed.get('summary', ''),
            'recommendations': parsed.get('recommendations', '')
        }
    
    def _get_default_quick_match(self) -> Dict:
        """Default response for quick match"""
        return {
            'match_score': 50,
            'skills_matched': [],
            'skills_missing': [],
            'summary': 'Unable to calculate match score',
            'recommendations': ''
        }

