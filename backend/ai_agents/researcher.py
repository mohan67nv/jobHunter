"""
Company Researcher Agent
Researches companies and provides comprehensive interview preparation with Q&A
"""
from typing import Dict, List
from ai_agents.base_agent import BaseAgent


class CompanyResearcher(BaseAgent):
    """Researches companies and generates comprehensive interview prep with Q&A"""
    
    def __init__(self, preferred_provider: str = "openai"):
        super().__init__(preferred_provider="openai")  # Use GPT-4o-mini for interview prep
    
    def process(self, company_name: str, job_title: str = None, 
                job_description: str = None, resume_text: str = None) -> Dict:
        """
        Research company and generate comprehensive interview preparation with Q&A
        
        Args:
            company_name: Name of company
            job_title: Job title (optional, for more specific insights)
            job_description: Job description (optional)
            resume_text: User's resume/CV text (optional, for personalized project questions)
            
        Returns:
            Dictionary with company insights, technical Q&A, behavioral Q&A, and HR Q&A
        """
        # Generate all sections using Perplexity
        company_info = self._generate_company_info(company_name, job_title, job_description)
        technical_qa = self._generate_technical_qa(company_name, job_title, job_description, resume_text)
        behavioral_qa = self._generate_behavioral_qa(company_name, job_title, job_description)
        hr_qa = self._generate_hr_qa(company_name, job_title, job_description)
        
        return {
            "company_info": company_info,
            "technical_qa": technical_qa,
            "behavioral_qa": behavioral_qa,
            "hr_qa": hr_qa
        }
    
    def _generate_company_info(self, company_name: str, job_title: str = None, 
                               job_description: str = None) -> Dict:
        """Generate comprehensive company information with company-specific Q&A"""
        job_context = f"\nJob Title: {job_title}" if job_title else ""
        jd_context = f"\nJob Description: {job_description[:1000]}" if job_description else ""
        
        prompt = f"""
Research {company_name} and provide comprehensive company information for interview preparation.

Company: {company_name}{job_context}{jd_context}

Return ONLY valid JSON with this exact structure:
{{
    "overview": {{
        "industry": "Industry name",
        "size": "Employee count",
        "headquarters": "Location",
        "founded": "Year",
        "description": "2-3 sentence company description",
        "mission": "Company mission statement",
        "products_services": ["Product 1", "Product 2", "Product 3"]
    }},
    "recent_news": [
        {{"title": "News headline", "date": "2024-XX-XX", "summary": "Brief summary", "relevance": "Why this matters for interview"}},
        {{"title": "News headline", "date": "2024-XX-XX", "summary": "Brief summary", "relevance": "Why this matters for interview"}},
        {{"title": "News headline", "date": "2024-XX-XX", "summary": "Brief summary", "relevance": "Why this matters for interview"}}
    ],
    "culture": {{
        "values": ["Value 1", "Value 2", "Value 3"],
        "work_environment": "Description of work environment",
        "work_life_balance": "Work-life balance insights",
        "diversity_inclusion": "D&I initiatives and culture",
        "employee_reviews_summary": "What employees say (pros and cons)"
    }},
    "company_qa": [
        {{
            "question": "Why do you want to work at {company_name}?",
            "answer": "Personalized answer mentioning specific products, values, and recent achievements. 3-4 sentences.",
            "talking_points": ["Point 1", "Point 2", "Point 3"],
            "reference": "Mention specific news or company initiative"
        }},
        {{
            "question": "What do you know about {company_name}'s products/services?",
            "answer": "Detailed answer about main products/services and market position. 3-4 sentences.",
            "talking_points": ["Point 1", "Point 2", "Point 3"],
            "reference": "Product names and recent launches"
        }},
        {{
            "question": "How do you see yourself contributing to {company_name}'s mission?",
            "answer": "Answer connecting role to company mission with specific examples. 3-4 sentences.",
            "talking_points": ["Point 1", "Point 2", "Point 3"],
            "reference": "Company mission and role alignment"
        }},
        {{
            "question": "What challenges do you think {company_name} is currently facing?",
            "answer": "Thoughtful analysis of industry challenges and company position. 3-4 sentences.",
            "talking_points": ["Point 1", "Point 2", "Point 3"],
            "reference": "Industry trends and recent news"
        }},
        {{
            "question": "What excites you most about this opportunity at {company_name}?",
            "answer": "Enthusiastic answer about role, team, technology, and growth. 3-4 sentences.",
            "talking_points": ["Point 1", "Point 2", "Point 3"],
            "reference": "Role specifics and company growth"
        }}
    ],
    "questions_to_ask": [
        {{"question": "What are the team's biggest priorities for the next 6 months?", "why_ask": "Shows strategic thinking"}},
        {{"question": "How does the company support professional development?", "why_ask": "Shows growth mindset"}},
        {{"question": "What does success look like in this role after 6 months?", "why_ask": "Shows results focus"}},
        {{"question": "How does the team collaborate and communicate?", "why_ask": "Shows team fit interest"}},
        {{"question": "What's the company culture around innovation and risk-taking?", "why_ask": "Shows cultural awareness"}}
    ]
}}

Use current, real information about {company_name}. Be specific and accurate.
"""
        
        response = self.generate(prompt, temperature=0.6, max_tokens=3000)
        parsed = self.parse_json_response(response)
        
        if not parsed:
            return self._get_default_company_info(company_name)
        
        return parsed
    
    def _generate_technical_qa(self, company_name: str, job_title: str = None, 
                               job_description: str = None, resume_text: str = None) -> List[Dict]:
        """Generate technical Q&A based on job description, Glassdoor insights, and candidate's resume"""
        job_context = f"\nJob Title: {job_title}" if job_title else ""
        jd_context = f"\nJob Description: {job_description}" if job_description else ""
        resume_context = f"\n\nCandidate's Resume/CV:\n{resume_text[:3000]}" if resume_text else ""
        
        prompt = f"""
Generate comprehensive technical interview questions and answers for {job_title} at {company_name}.

Company: {company_name}{job_context}{jd_context}{resume_context}

IMPORTANT: Include THREE types of questions:

1. GLASSDOOR/REAL CANDIDATE QUESTIONS (5-7 questions)
   - Search your knowledge for actual interview questions asked at {company_name}
   - Include questions from Glassdoor, Blind, LeetCode Discuss for this company
   - Mark these with "source": "glassdoor" or "source": "candidate_report"

2. JOB-SPECIFIC TECHNICAL QUESTIONS (5-7 questions)
   - Based on job description requirements
   - Role-specific technical depth

3. CANDIDATE'S PROJECT/EXPERIENCE QUESTIONS (5-7 questions) {"- ONLY if resume provided" if resume_text else ""}
   - Questions about candidate's specific projects mentioned in resume
   - "Tell me about your [project name]" questions
   - Technical deep-dives into their experience
   - How to explain their projects effectively
   - Potential challenges interviewer might probe

Return ONLY valid JSON array with 15-20 questions total:
[
    {{
        "question": "Specific technical question",
        "answer": "Comprehensive answer with examples, code snippets if relevant, best practices. 4-6 sentences minimum.",
        "difficulty": "Easy|Medium|Hard",
        "category": "System Design|Algorithms|ML|Cloud|Database|Project-Experience|Company-Specific",
        "source": "glassdoor|job_description|candidate_project",
        "key_points": ["Key point 1", "Key point 2", "Key point 3"],
        "follow_ups": ["Potential follow-up question 1", "Potential follow-up question 2"],
        "project_context": "Name of candidate's project (if source is candidate_project)",
        "explanation_approach": "How to explain this effectively (for project questions)"
    }}
]

For GLASSDOOR questions:
- Include actual questions reported by candidates
- Mention company-specific interview patterns
- Include coding questions if they use specific platforms (LeetCode, HackerRank)

For PROJECT questions (if resume provided):
- Reference specific project names from resume
- Ask about technical decisions made
- Probe architecture and scalability
- Ask about challenges faced
- Provide guidance on best way to explain the project
- Suggest metrics/results to highlight

Make all answers detailed, practical, and demonstrate expertise.
"""
        
        response = self.generate(prompt, temperature=0.5, max_tokens=6000)
        parsed = self.parse_json_response(response)
        
        if not parsed or not isinstance(parsed, list):
            return self._get_default_technical_qa(job_title)
        
        return parsed
    
    def _generate_behavioral_qa(self, company_name: str, job_title: str = None, 
                                job_description: str = None) -> List[Dict]:
        """Generate behavioral Q&A using STAR method"""
        job_context = f"\nJob Title: {job_title}" if job_title else ""
        jd_context = f"\nJob Description: {job_description[:800]}" if job_description else ""
        
        prompt = f"""
Generate behavioral interview questions with STAR method answers for this role at {company_name}.

Company: {company_name}{job_context}{jd_context}

Return ONLY valid JSON array with 10-12 behavioral questions:
[
    {{
        "question": "Behavioral question (e.g., 'Tell me about a time when...')",
        "answer": "Complete STAR format answer demonstrating the competency. 5-7 sentences.",
        "situation": "Context and background (1-2 sentences)",
        "task": "What needed to be accomplished (1 sentence)",
        "action": "Specific actions taken (2-3 sentences with details)",
        "result": "Outcome with metrics if possible (1-2 sentences)",
        "competency": "Leadership|Teamwork|Problem-Solving|Communication|Adaptability|Initiative|Conflict-Resolution",
        "tips": ["Tip 1 for answering well", "Tip 2"]
    }}
]

Include questions about:
- Leadership and team management
- Handling conflict and difficult situations
- Problem-solving and decision-making
- Adaptability and change management
- Communication and collaboration
- Taking initiative and ownership
- Handling failure and learning
- Time management and prioritization
- Customer focus
- Innovation and creativity

Make answers realistic, detailed, and impressive. Use specific examples with measurable results.
"""
        
        response = self.generate(prompt, temperature=0.6, max_tokens=4000)
        parsed = self.parse_json_response(response)
        
        if not parsed or not isinstance(parsed, list):
            return self._get_default_behavioral_qa()
        
        return parsed
    
    def _generate_hr_qa(self, company_name: str, job_title: str = None, 
                        job_description: str = None) -> List[Dict]:
        """Generate HR and general interview Q&A"""
        job_context = f"\nJob Title: {job_title}" if job_title else ""
        
        prompt = f"""
Generate HR and general interview questions with strategic answers for this role at {company_name}.

Company: {company_name}{job_context}

Return ONLY valid JSON array with 8-10 HR questions:
[
    {{
        "question": "Common HR question",
        "answer": "Strategic answer that positions candidate well. 3-5 sentences.",
        "category": "Career Goals|Strengths-Weaknesses|Motivation|Salary|Work Style|Conflict|Availability",
        "dos": ["Do 1", "Do 2", "Do 3"],
        "donts": ["Don't 1", "Don't 2"],
        "example_answer": "Specific example answer tailored to role"
    }}
]

Include questions about:
- Career goals and motivation
- Strengths and weaknesses
- Salary expectations
- Work style and preferences
- Why leaving current role
- Handling work pressure
- Availability and notice period
- Long-term career plans
- Gaps in resume (if applicable)
- What makes you unique

Provide honest but strategic answers that position the candidate positively.
"""
        
        response = self.generate(prompt, temperature=0.6, max_tokens=3000)
        parsed = self.parse_json_response(response)
        
        if not parsed or not isinstance(parsed, list):
            return self._get_default_hr_qa()
        
        return parsed
    
    def _get_default_company_info(self, company_name: str) -> Dict:
        """Fallback company info if generation fails"""
        return {
            "overview": {
                "industry": "Technology",
                "size": "Unknown",
                "headquarters": "Unknown",
                "founded": "Unknown",
                "description": f"{company_name} is a company in the technology sector.",
                "mission": "Information not available",
                "products_services": ["Information not available"]
            },
            "recent_news": [],
            "culture": {
                "values": ["Innovation", "Quality", "Collaboration"],
                "work_environment": "Professional",
                "work_life_balance": "Standard",
                "diversity_inclusion": "Information not available",
                "employee_reviews_summary": "Research on Glassdoor recommended"
            },
            "company_qa": [
                {
                    "question": f"Why do you want to work at {company_name}?",
                    "answer": f"Research {company_name}'s products, values, and recent achievements to provide a personalized answer.",
                    "talking_points": ["Company mission", "Products/services", "Growth opportunities"],
                    "reference": "Visit company website and news"
                }
            ],
            "questions_to_ask": [
                {"question": "What are the team's biggest priorities?", "why_ask": "Shows strategic thinking"},
                {"question": "How does the company support professional development?", "why_ask": "Shows growth mindset"}
            ]
        }
    
    def _get_default_technical_qa(self, job_title: str = None) -> List[Dict]:
        """Fallback technical Q&A if generation fails"""
        return [
            {
                "question": "Describe a challenging technical problem you solved recently.",
                "answer": "Use STAR method: Describe the situation, technical challenge, your approach, technologies used, and measurable results.",
                "difficulty": "Medium",
                "category": "Problem-Solving",
                "key_points": ["Problem analysis", "Solution design", "Implementation", "Results"],
                "follow_ups": ["What would you do differently?", "What did you learn?"]
            }
        ]
    
    def _get_default_behavioral_qa(self) -> List[Dict]:
        """Fallback behavioral Q&A if generation fails"""
        return [
            {
                "question": "Tell me about a time when you had to work with a difficult team member.",
                "answer": "Use STAR format to describe the situation, your approach to communication, actions taken to resolve issues, and positive outcome.",
                "situation": "Describe the context and difficulty",
                "task": "What needed to be accomplished",
                "action": "Steps you took to address the situation",
                "result": "Positive outcome achieved",
                "competency": "Conflict-Resolution",
                "tips": ["Stay professional", "Focus on solution", "Show empathy"]
            }
        ]
    
    def _get_default_hr_qa(self) -> List[Dict]:
        """Fallback HR Q&A if generation fails"""
        return [
            {
                "question": "Where do you see yourself in 5 years?",
                "answer": "Focus on professional growth within the role and company, showing ambition balanced with commitment.",
                "category": "Career Goals",
                "dos": ["Show ambition", "Align with company", "Be realistic"],
                "donts": ["Don't say 'your job'", "Don't be vague", "Don't mention leaving"],
                "example_answer": "I see myself growing as a technical expert and potentially leading projects, while continuously learning and contributing to the company's success."
            }
        ]
    
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
