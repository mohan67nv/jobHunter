"""
Company Researcher Agent
Researches companies and provides interview preparation insights
"""
from typing import Dict, List
from ai_agents.base_agent import BaseAgent


class CompanyResearcher(BaseAgent):
    """Researches companies and generates interview insights"""
    
    def process(self, company_name: str, job_title: str = None, 
                job_description: str = None) -> Dict:
        """
        Research company and generate insights
        
        Args:
            company_name: Name of company
            job_title: Job title (optional, for more specific insights)
            job_description: Job description (optional)
            
        Returns:
            Dictionary with company insights and interview tips
        """
        # Note: In production, this would integrate with web search APIs
        # For now, we'll use AI's knowledge base
        
        job_context = f"\nJob Title: {job_title}" if job_title else ""
        jd_context = f"\nJob Description: {job_description[:1000]}" if job_description else ""
        
        prompt = f"""
Provide comprehensive company research and interview preparation for a job application. Return ONLY valid JSON:

{{
    "company_overview": {{
        "industry": "Automotive Technology",
        "size": "100,000+ employees",
        "headquarters": "Munich, Germany",
        "founded": "1916",
        "description": "Brief company description"
    }},
    "recent_news": [
        "News item 1 (last 6 months)",
        "News item 2",
        "News item 3"
    ],
    "company_culture": {{
        "values": ["Innovation", "Quality", "Sustainability"],
        "work_environment": "Engineering-focused, collaborative",
        "work_life_balance": "Good, flexible hours"
    }},
    "interview_tips": [
        "Tip 1: Focus on...",
        "Tip 2: Prepare examples of...",
        "Tip 3: Show knowledge of..."
    ],
    "likely_questions": [
        "Tell me about a time when you solved a complex technical problem",
        "How do you stay current with technology trends?",
        "Why do you want to work for [company]?"
    ],
    "technical_focus_areas": [
        "Machine Learning",
        "Cloud Architecture",
        "System Design"
    ],
    "salary_insights": {{
        "range": "€70,000 - €95,000",
        "factors": ["Experience level", "Location", "Skills"],
        "negotiation_tips": "Research market rates, highlight unique skills"
    }},
    "growth_opportunities": [
        "Career development programs",
        "Internal mobility",
        "Learning budget"
    ]
}}

Company: {company_name}{job_context}{jd_context}

Provide accurate, relevant information based on your knowledge. If uncertain, indicate with "[Estimated]" or "[Typical for industry]".
"""
        
        response = self.generate(prompt, temperature=0.5, max_tokens=2000)
        
        if not response:
            return self._get_default_research(company_name)
        
        parsed = self.parse_json_response(response)
        
        if not parsed:
            return self._get_default_research(company_name)
        
        research = self._normalize_research(parsed, company_name)
        
        return research
    
    def generate_interview_questions(self, job_description: str, company_name: str) -> List[str]:
        """
        Generate likely interview questions for specific job
        
        Args:
            job_description: Full job description
            company_name: Company name
            
        Returns:
            List of likely interview questions
        """
        prompt = f"""
Based on this job description, generate 15 likely interview questions (mix of technical, behavioral, and company-specific).

Company: {company_name}
Job Description: {job_description[:2000]}

Return as JSON array:
{{
    "questions": [
        "Question 1",
        "Question 2",
        ...
    ]
}}

Include:
- 5 technical questions based on required skills
- 5 behavioral questions (STAR method applicable)
- 3 company-specific questions
- 2 situational/problem-solving questions
"""
        
        response = self.generate(prompt, temperature=0.6)
        
        if not response:
            return self._get_default_questions()
        
        parsed = self.parse_json_response(response)
        
        if parsed and 'questions' in parsed:
            return parsed['questions']
        
        return self._get_default_questions()
    
    def _normalize_research(self, data: Dict, company_name: str) -> Dict:
        """Ensure research data has all required fields"""
        return {
            'company_name': company_name,
            'company_overview': data.get('company_overview', {}),
            'recent_news': data.get('recent_news', []),
            'company_culture': data.get('company_culture', {}),
            'interview_tips': data.get('interview_tips', []),
            'likely_questions': data.get('likely_questions', []),
            'technical_focus_areas': data.get('technical_focus_areas', []),
            'salary_insights': data.get('salary_insights', {}),
            'growth_opportunities': data.get('growth_opportunities', []),
        }
    
    def _get_default_research(self, company_name: str) -> Dict:
        """Return default research structure when AI fails"""
        return {
            'company_name': company_name,
            'company_overview': {
                'description': f'Research unavailable for {company_name}'
            },
            'recent_news': ['Company research unavailable'],
            'company_culture': {},
            'interview_tips': [
                'Research the company thoroughly',
                'Prepare specific examples of your work',
                'Practice behavioral questions'
            ],
            'likely_questions': self._get_default_questions(),
            'technical_focus_areas': [],
            'salary_insights': {},
            'growth_opportunities': [],
        }
    
    def _get_default_questions(self) -> List[str]:
        """Return default interview questions"""
        return [
            "Tell me about yourself and your background",
            "Why are you interested in this position?",
            "What are your greatest strengths?",
            "Describe a challenging project you worked on",
            "How do you handle tight deadlines?",
            "Tell me about a time you worked in a team",
            "What are your salary expectations?",
            "Where do you see yourself in 5 years?",
            "Why should we hire you?",
            "Do you have any questions for us?"
        ]
