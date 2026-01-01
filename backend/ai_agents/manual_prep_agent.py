"""
Manual Prep AI Agent
Advanced interview preparation using DeepSeek Reasoner + GPT-5-mini
Generates comprehensive preparation materials from job URL and company details
"""
from typing import Dict, List, Optional
import json
from ai_agents.base_agent import BaseAgent
from ai_agents.model_config import get_model_config
from utils.logger import setup_logger

logger = setup_logger(__name__)


class ResearchAgent(BaseAgent):
    """Simple concrete implementation of BaseAgent for company research"""
    def process(self, prompt: str) -> str:
        """Process wrapper for BaseAgent"""
        return self.generate(prompt, temperature=0.3, max_tokens=2000)


class ManualPrepAgent(BaseAgent):
    """
    Advanced interview preparation agent using multi-model approach:
    - DeepSeek Reasoner: Deep analysis and strategic insights
    - GPT-5-mini: Company research and latest information
    - DeepSeek Chat: Fast structured data generation
    """
    
    def __init__(self):
        # Initialize with DeepSeek Reasoner for primary processing
        config = get_model_config('MultiLayerATS_Layer3')  # DeepSeek Reasoner
        super().__init__(preferred_provider=config["provider"], model=config["model"])
        
        # Secondary agent for company research (GPT-5-mini)
        research_config = get_model_config('CompanyResearcher')
        self.research_agent = ResearchAgent(
            preferred_provider=research_config['provider'],
            model=research_config['model']
        )
        
        logger.info("✅ ManualPrepAgent initialized (DeepSeek Reasoner + GPT-5-mini)")
    
    def process(self, company_name: str, job_title: Optional[str] = None, 
                job_description: Optional[str] = None, job_url: Optional[str] = None,
                resume_text: Optional[str] = None) -> Dict:
        """
        Generate comprehensive interview preparation materials
        
        Args:
            company_name: Company name (required)
            job_title: Job title (optional)
            job_description: Job description text (optional)
            job_url: Job posting URL (optional, for reference)
            resume_text: User's resume for personalized preparation
            
        Returns:
            Dictionary with all preparation materials
        """
        logger.info(f"🎯 Generating advanced prep for {company_name} - {job_title}")
        
        # Step 1: Company research using GPT-5-mini (latest data)
        logger.info("  1/5: Researching company (GPT-5-mini)...")
        company_insights = self._research_company(company_name, job_title, job_description)
        
        # Step 2: Technical Q&A using DeepSeek Reasoner (deep reasoning)
        logger.info("  2/5: Generating technical Q&A (DeepSeek Reasoner)...")
        technical_qa = self._generate_technical_qa(
            company_name, job_title, job_description, resume_text, company_insights
        )
        
        # Step 3: Behavioral Q&A with STAR examples
        logger.info("  3/5: Creating behavioral Q&A (DeepSeek Reasoner)...")
        behavioral_qa = self._generate_behavioral_qa(
            company_name, job_title, job_description, company_insights
        )
        
        # Step 4: HR/Salary Q&A
        logger.info("  4/5: Preparing HR questions (GPT-5-mini)...")
        hr_qa = self._generate_hr_qa(company_name, job_title, company_insights)
        
        # Step 5: Key talking points and strategic tips
        logger.info("  5/5: Creating strategic insights (DeepSeek Reasoner)...")
        talking_points, prep_tips = self._generate_strategic_insights(
            company_name, job_title, job_description, technical_qa, behavioral_qa, company_insights
        )
        
        logger.info("✅ Manual prep generation complete")
        
        return {
            "company_insights": company_insights,
            "technical_qa": technical_qa,
            "behavioral_qa": behavioral_qa,
            "hr_qa": hr_qa,
            "key_talking_points": talking_points,
            "preparation_tips": prep_tips
        }
    
    def _research_company(self, company_name: str, job_title: Optional[str] = None, 
                         job_description: Optional[str] = None) -> Dict:
        """Research company using GPT-5-mini for latest information"""
        
        job_context = f"\nJob Title: {job_title}" if job_title else ""
        jd_context = f"\nJob Description: {job_description[:1000]}" if job_description else ""
        
        prompt = f"""
Research {company_name} and provide comprehensive company intelligence.{job_context}{jd_context}

Provide detailed information in JSON format:
{{
    "overview": "Company overview and what they do",
    "size": "Company size (employees, revenue if known)",
    "industry": "Industry sector",
    "culture": "Company culture and values (specific examples)",
    "recent_news": ["Recent news item 1", "Recent news item 2", "Recent news item 3"],
    "products_services": ["Main product/service 1", "product 2", "product 3"],
    "tech_stack": ["Known technology 1", "technology 2", "technology 3"],
    "competitors": ["Competitor 1", "Competitor 2", "Competitor 3"],
    "growth_stage": "Startup/Growth/Mature/Enterprise",
    "strengths": ["Strength 1", "Strength 2"],
    "challenges": ["Challenge 1", "Challenge 2"],
    "why_work_here": ["Reason 1", "Reason 2", "Reason 3"]
}}

Be specific and factual. Use latest available information.
"""
        
        response = self.research_agent.generate(prompt, temperature=0.3, max_tokens=2000)
        result = self.parse_json_response(response) if response else {}
        
        return result or {
            "overview": f"Leading company in their industry",
            "culture": "Dynamic and innovative work environment",
            "recent_news": [],
            "products_services": [],
            "tech_stack": [],
            "why_work_here": ["Great growth opportunities", "Innovative projects"]
        }
    
    def _generate_technical_qa(self, company_name: str, job_title: Optional[str],
                               job_description: Optional[str], resume_text: Optional[str],
                               company_insights: Dict) -> List[Dict]:
        """Generate technical Q&A using DeepSeek Reasoner for deep analysis"""
        
        jd_excerpt = job_description[:2000] if job_description else "General role"
        resume_excerpt = resume_text[:2000] if resume_text else "Experienced professional"
        tech_stack = ", ".join(company_insights.get('tech_stack', [])[:5])
        
        prompt = f"""
You are an expert technical interviewer for {company_name}.
Job Title: {job_title}
Company Tech Stack: {tech_stack}

Job Description: {jd_excerpt}
Candidate Resume: {resume_excerpt}

Generate 10 technical interview questions with detailed answers.
Think deeply about what {company_name} would actually ask for this role.

Return JSON array:
[
    {{
        "question": "Specific technical question",
        "difficulty": "Medium/Hard",
        "topics": ["topic1", "topic2"],
        "answer": "Comprehensive answer with code examples if relevant",
        "follow_up": "Likely follow-up question",
        "why_they_ask": "Why this company cares about this"
    }}
]

Make questions realistic, specific to the role, and progressively challenging.
Include system design, coding, and conceptual questions.
"""
        
        response = self.generate(prompt, temperature=0.6, max_tokens=3000)
        result = self.parse_json_response(response) if response else []
        
        return result[:10] if result else [
            {
                "question": f"How would you approach a {job_title} problem at {company_name}?",
                "difficulty": "Medium",
                "topics": ["problem-solving"],
                "answer": "I would start by understanding requirements...",
                "follow_up": "How would you scale this?",
                "why_they_ask": "Tests practical problem-solving"
            }
        ]
    
    def _generate_behavioral_qa(self, company_name: str, job_title: Optional[str],
                                job_description: Optional[str], company_insights: Dict) -> List[Dict]:
        """Generate behavioral Q&A with STAR framework examples"""
        
        culture = company_insights.get('culture', 'Collaborative environment')
        values = company_insights.get('why_work_here', [])
        
        prompt = f"""
You are preparing someone for behavioral interviews at {company_name}.
Job Title: {job_title}
Company Culture: {culture}
Company Values: {', '.join(values[:3])}

Generate 8 behavioral interview questions with STAR framework answers.
Make them specific to {company_name}'s culture and this role.

Return JSON array:
[
    {{
        "question": "Behavioral question",
        "category": "Leadership/Teamwork/Conflict/Failure/Success",
        "star_example": {{
            "situation": "Context and background",
            "task": "What needed to be done",
            "action": "Specific actions taken",
            "result": "Measurable outcome"
        }},
        "key_takeaway": "What this demonstrates",
        "company_relevance": "Why this matters to {company_name}"
    }}
]

Focus on: leadership, teamwork, conflict resolution, innovation, and handling pressure.
"""
        
        response = self.generate(prompt, temperature=0.7, max_tokens=2500)
        result = self.parse_json_response(response) if response else []
        
        return result[:8] if result else [
            {
                "question": "Tell me about a time you faced a challenge",
                "category": "Problem Solving",
                "star_example": {
                    "situation": "In my previous role...",
                    "task": "I needed to...",
                    "action": "I took these steps...",
                    "result": "We achieved..."
                },
                "key_takeaway": "Demonstrates resilience",
                "company_relevance": f"Shows alignment with {company_name} values"
            }
        ]
    
    def _generate_hr_qa(self, company_name: str, job_title: Optional[str],
                       company_insights: Dict) -> List[Dict]:
        """Generate HR and salary negotiation questions"""
        
        prompt = f"""
Generate 6 HR/salary interview questions and answers for {company_name} - {job_title}.

Return JSON array:
[
    {{
        "question": "HR question",
        "category": "Salary/Benefits/Culture/Growth/Work-Life",
        "answer": "Professional answer with strategy",
        "tips": ["Tip 1", "Tip 2"],
        "red_flags": ["What to avoid saying"]
    }}
]

Include: salary negotiation, why this company, career goals, work-life balance.
"""
        
        response = self.research_agent.generate(prompt, temperature=0.5, max_tokens=1500)
        result = self.parse_json_response(response) if response else []
        
        return result[:6] if result else []
    
    def _generate_strategic_insights(self, company_name: str, job_title: Optional[str],
                                    job_description: Optional[str], technical_qa: List,
                                    behavioral_qa: List, company_insights: Dict) -> tuple:
        """Generate key talking points and preparation tips using DeepSeek Reasoner"""
        
        prompt = f"""
Create strategic interview preparation for {company_name} - {job_title}.

Company: {company_name}
Role: {job_title}
Culture: {company_insights.get('culture', 'N/A')}
Recent News: {', '.join(company_insights.get('recent_news', [])[:2])}

Based on the company and role, provide:

1. Key Talking Points - What to emphasize in interview
2. Preparation Tips - Specific things to prepare/research

Return JSON:
{{
    "key_talking_points": [
        {{"point": "Talking point 1", "why": "Why it matters", "how_to_mention": "How to bring it up"}},
        {{"point": "Talking point 2", "why": "Why it matters", "how_to_mention": "When to mention"}}
    ],
    "preparation_tips": [
        {{"tip": "Preparation tip 1", "category": "Research/Practice/Materials", "priority": "High"}},
        {{"tip": "Preparation tip 2", "category": "Category", "priority": "Medium"}}
    ]
}}

Think strategically about what will make the candidate stand out at {company_name}.
"""
        
        response = self.generate(prompt, temperature=0.7, max_tokens=2000)
        result = self.parse_json_response(response) if response else {}
        
        talking_points = result.get('key_talking_points', [
            {
                "point": f"Experience relevant to {job_title}",
                "why": "Demonstrates capability",
                "how_to_mention": "When discussing background"
            }
        ])
        
        prep_tips = result.get('preparation_tips', [
            {
                "tip": f"Research {company_name}'s latest products",
                "category": "Research",
                "priority": "High"
            }
        ])
        
        return talking_points, prep_tips
