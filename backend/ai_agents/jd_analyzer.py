"""
Job Description Analyzer Agent
Extracts structured information from job descriptions
"""
from typing import Dict, List
from ai_agents.base_agent import BaseAgent
from ai_agents.model_config import get_model_config


class JDAnalyzer(BaseAgent):
    """Analyzes job descriptions and extracts key information"""
    
    def __init__(self):
        config = get_model_config("JDAnalyzer")
        super().__init__(preferred_provider=config["provider"], model=config["model"])
    
    def process(self, job_description: str) -> Dict:
        """
        Analyze job description and extract structured information
        
        Args:
            job_description: Full job description text
            
        Returns:
            Dictionary with extracted information
        """
        prompt = f"""
Analyze this job description and extract structured information. Return ONLY valid JSON with this exact structure:

{{
    "required_skills": ["skill1", "skill2", ...],
    "nice_to_have": ["skill1", "skill2", ...],
    "experience_years": 5,
    "tech_stack": ["tech1", "tech2", ...],
    "must_haves": ["requirement1", "requirement2", ...],
    "responsibilities": ["responsibility1", "responsibility2", ...],
    "education_required": "Bachelor's degree in Computer Science or equivalent",
    "language_requirements": ["German (fluent)", "English (business level)"],
    "job_type": "full-time",
    "remote_type": "hybrid",
    "salary_range": "€70,000 - €90,000",
    "benefits": ["benefit1", "benefit2", ...]
}}

Job Description:
{job_description}

Extract all relevant information. If a field is not mentioned, use null or empty array. Be thorough and precise.
"""
        
        response = self.generate(prompt, temperature=0.3)
        
        if not response:
            return self._get_default_analysis()
        
        parsed = self.parse_json_response(response)
        
        if not parsed:
            return self._get_default_analysis()
        
        # Ensure all required fields exist
        analysis = self._normalize_analysis(parsed)
        
        return analysis
    
    def _normalize_analysis(self, data: Dict) -> Dict:
        """Ensure analysis has all required fields"""
        return {
            'required_skills': data.get('required_skills', []),
            'nice_to_have': data.get('nice_to_have', []),
            'experience_years': data.get('experience_years', 0),
            'tech_stack': data.get('tech_stack', []),
            'must_haves': data.get('must_haves', []),
            'responsibilities': data.get('responsibilities', []),
            'education_required': data.get('education_required', ''),
            'language_requirements': data.get('language_requirements', []),
            'job_type': data.get('job_type', ''),
            'remote_type': data.get('remote_type', ''),
            'salary_range': data.get('salary_range', ''),
            'benefits': data.get('benefits', []),
        }
    
    def _get_default_analysis(self) -> Dict:
        """Return default analysis structure when AI fails"""
        return {
            'required_skills': [],
            'nice_to_have': [],
            'experience_years': 0,
            'tech_stack': [],
            'must_haves': [],
            'responsibilities': [],
            'education_required': '',
            'language_requirements': [],
            'job_type': '',
            'remote_type': '',
            'salary_range': '',
            'benefits': [],
        }
