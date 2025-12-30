"""
Resume-Job Matcher Agent
Calculates match score and identifies skill gaps
"""
from typing import Dict, List
from ai_agents.base_agent import BaseAgent


class ResumeMatcher(BaseAgent):
    """Matches resume to job requirements and calculates compatibility"""
    
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
            'experience_match': 'Unable to determine',
            'education_match': 'Unable to determine',
            'strengths': [],
            'concerns': ['AI analysis unavailable'],
            'overall_assessment': 'Manual review recommended',
        }
