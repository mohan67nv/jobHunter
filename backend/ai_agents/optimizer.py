"""
Application Optimizer Agent
Generates tailored resumes and cover letters
"""
from typing import Dict, List
from ai_agents.base_agent import BaseAgent
from ai_agents.model_config import get_model_config


class ApplicationOptimizer(BaseAgent):
    """Optimizes resume and generates tailored application materials"""
    
    def __init__(self):
        config = get_model_config("ApplicationOptimizer")
        super().__init__(preferred_provider=config["provider"], model=config["model"])
    
    def generate_tailored_resume(self, resume_text: str, job_description: str, 
                                 match_analysis: Dict) -> str:
        """
        Generate tailored resume bullets for specific job
        
        Args:
            resume_text: Original resume text
            job_description: Target job description
            match_analysis: Match analysis from ResumeMatcher
            
        Returns:
            Tailored resume content
        """
        matching_skills = ', '.join([s['skill'] for s in match_analysis.get('matching_skills', [])])
        missing_skills = ', '.join(match_analysis.get('missing_skills', []))
        
        prompt = f"""
Create tailored resume bullets for this job application. Emphasize matching skills and experiences.

Original Resume:
{resume_text[:2000]}

Job Description:
{job_description[:2000]}

Matching Skills to Emphasize: {matching_skills}
Skills to Naturally Integrate (if applicable): {missing_skills}

Generate 5-7 powerful resume bullets that:
1. Emphasize experiences matching the job requirements
2. Use action verbs and quantify achievements
3. Naturally incorporate relevant keywords
4. Avoid keyword stuffing
5. Maintain authenticity

Return bullets as plain text, one per line, starting with "•".
"""
        
        response = self.generate(prompt, temperature=0.7, max_tokens=800)
        
        return response if response else "• Unable to generate tailored resume"
    
    def generate_cover_letter(self, resume_text: str, job_title: str, 
                             company_name: str, job_description: str,
                             match_analysis: Dict, user_info: Dict = None) -> str:
        """
        Generate personalized cover letter
        
        Args:
            resume_text: User's resume
            job_title: Target job title
            company_name: Target company
            job_description: Full job description
            match_analysis: Match analysis data
            user_info: User profile information
            
        Returns:
            Cover letter text
        """
        user_name = user_info.get('name', '[Your Name]') if user_info else '[Your Name]'
        
        prompt = f"""
Write a compelling, professional cover letter for this job application.

Candidate: {user_name}
Position: {job_title}
Company: {company_name}

Key Qualifications from Resume:
{resume_text[:1500]}

Job Requirements:
{job_description[:1500]}

Write a 3-paragraph cover letter that:
1. Opening: Express enthusiasm and mention how you learned about the role
2. Body: Highlight 2-3 key achievements that directly match job requirements
3. Closing: Express interest in interview and next steps

Guidelines:
- Be authentic and professional
- Use specific examples
- Show knowledge of company/industry
- Keep it concise (300-400 words)
- Avoid clichés

Return the cover letter in plain text format, ready to use.
"""
        
        response = self.generate(prompt, temperature=0.7, max_tokens=1000)
        
        return response if response else f"Dear Hiring Manager at {company_name},\n\nI am writing to express my strong interest in the {job_title} position.\n\n[Cover letter generation unavailable]"
    
    def process(self, resume_text: str, job_data: Dict, match_analysis: Dict, 
                user_info: Dict = None, generate_type: str = "both") -> Dict:
        """
        Generate optimized application materials
        
        Args:
            resume_text: User's resume
            job_data: Job information dict
            match_analysis: Match analysis from ResumeMatcher
            user_info: User profile info
            generate_type: "resume", "cover_letter", or "both"
            
        Returns:
            Dictionary with generated content
        """
        result = {}
        
        job_description = job_data.get('description', '')
        job_title = job_data.get('title', '')
        company_name = job_data.get('company', '')
        
        if generate_type in ["resume", "both"]:
            result['tailored_resume'] = self.generate_tailored_resume(
                resume_text, job_description, match_analysis
            )
        
        if generate_type in ["cover_letter", "both"]:
            result['tailored_cover_letter'] = self.generate_cover_letter(
                resume_text, job_title, company_name, 
                job_description, match_analysis, user_info
            )
        
        # Generate keywords to add
        result['keywords_to_add'] = self._suggest_keywords(
            resume_text, job_description, match_analysis
        )
        
        return result
    
    def _suggest_keywords(self, resume_text: str, job_description: str, 
                         match_analysis: Dict) -> List[str]:
        """Suggest keywords to naturally integrate into resume"""
        missing_skills = match_analysis.get('missing_skills', [])
        
        if not missing_skills:
            return []
        
        # Return top missing skills that are most important
        return missing_skills[:5]
