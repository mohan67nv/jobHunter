"""
Advanced Resume Optimizer
Generates JD-specific summaries, experience bullets, and skills recommendations
"""
import json
import re
from typing import Dict, List
from ai_agents.base_agent import BaseAgent
from utils.logger import setup_logger

logger = setup_logger(__name__)


class ResumeOptimizer(BaseAgent):
    """
    Advanced resume optimization using GPT-5-mini
    - Extracts CV experience sections with metrics
    - Generates JD-specific professional summary
    - Creates experience bullets mapped to actual CV companies
    - Suggests skills for Skills section
    """
    
    def __init__(self):
        # Use GPT-5-mini for best quality
        super().__init__(preferred_provider="openai", model="gpt-5-mini")
        logger.info("✅ ResumeOptimizer initialized with GPT-5-mini")
    
    def process(self, resume_text: str, job_description: str, missing_keywords: List[str]) -> Dict:
        """
        Main processing: Generate all optimization suggestions
        """
        # Extract CV structure
        cv_analysis = self._extract_cv_structure(resume_text)
        
        # Generate JD-specific summary
        summary = self._generate_jd_summary(resume_text, job_description, cv_analysis)
        
        # Generate experience bullets mapped to CV companies
        experience_bullets = self._generate_experience_bullets(
            resume_text, job_description, missing_keywords, cv_analysis
        )
        
        # Generate skills section suggestions
        skills_suggestions = self._generate_skills_suggestions(
            resume_text, job_description, missing_keywords
        )
        
        return {
            "jd_specific_summary": summary,
            "experience_bullet_suggestions": experience_bullets,
            "skills_section_suggestions": skills_suggestions,
            "cv_analysis": cv_analysis
        }
    
    def _extract_cv_structure(self, resume_text: str) -> Dict:
        """
        Extract CV structure: experience, metrics, skills, education
        """
        prompt = f"""Extract structured information from this resume. Return ONLY valid JSON:

Resume:
{resume_text[:4000]}

Extract:
{{
    "current_role": "Senior Data Scientist at Company X",
    "years_experience": 5,
    "companies": [
        {{
            "name": "Company X",
            "role": "Senior Data Scientist",
            "duration": "2021-Present",
            "key_achievements": [
                "Reduced inference time by 40%",
                "Deployed 12 ML models"
            ],
            "technologies": ["Python", "TensorFlow", "AWS"]
        }}
    ],
    "quantified_achievements": [
        "40% reduction in inference time",
        "Improved accuracy by 15%",
        "Processed 1M+ records daily"
    ],
    "education": {{
        "degree": "MSc Data Analytics",
        "institution": "University X",
        "year": "2020"
    }},
    "current_skills": ["Python", "Machine Learning", "SQL", "AWS"],
    "certifications": []
}}

Extract ALL companies, roles, and quantified achievements. Include specific metrics (%, numbers, time saved, etc.).
"""
        
        response = self.generate(prompt, temperature=0.3)
        
        if not response:
            logger.error("❌ Failed to extract CV structure")
            return self._get_default_cv_structure()
        
        parsed = self.parse_json_response(response)
        
        if not parsed:
            logger.error("❌ Failed to parse CV structure JSON")
            return self._get_default_cv_structure()
        
        logger.info(f"✅ Extracted CV: {len(parsed.get('companies', []))} companies, "
                   f"{len(parsed.get('quantified_achievements', []))} metrics")
        
        return parsed
    
    def _generate_jd_summary(self, resume_text: str, job_description: str, cv_analysis: Dict) -> Dict:
        """
        Generate JD-specific professional summary using actual CV metrics
        """
        current_role = cv_analysis.get('current_role', 'Professional')
        years_exp = cv_analysis.get('years_experience', 0)
        achievements = cv_analysis.get('quantified_achievements', [])[:5]
        education = cv_analysis.get('education', {})
        
        achievements_str = '\n'.join([f"- {ach}" for ach in achievements])
        
        prompt = f"""Write a JD-specific professional summary (2-3 sentences) for this candidate.

Job Description (extract key requirements):
{job_description[:1500]}

Candidate's Profile:
- Current Role: {current_role}
- Experience: {years_exp} years
- Education: {education.get('degree', 'N/A')} from {education.get('institution', 'N/A')}
- Key Achievements:
{achievements_str}

Return ONLY valid JSON:
{{
    "summary": "Results-oriented Senior Data Scientist with MSc in quantitative discipline and 5+ years implementing business-focused analytics solutions. Expert in Python, R, and modern statistical concepts with proven track record of reducing inference time by 40% and deploying 12+ production ML models. Skilled in model supervision, data reviews, and optimizing analytics frameworks to drive informed decision-making.",
    "key_metrics_used": [
        "5+ years experience",
        "40% inference time reduction",
        "12+ production models"
    ],
    "jd_keywords_incorporated": [
        "quantitative discipline",
        "analytics solutions",
        "business-focused",
        "model supervision",
        "informed decision-making"
    ]
}}

REQUIREMENTS:
1. Use candidate's REAL metrics from their CV (don't invent numbers)
2. Incorporate JD keywords naturally (analytics solutions, quantitative discipline, etc.)
3. Keep it 2-3 sentences max
4. Lead with role/title match from JD
5. Balance qualifications with achievements
"""
        
        response = self.generate(prompt, temperature=0.4)
        
        if not response:
            logger.error("❌ Failed to generate summary")
            return {"summary": "", "key_metrics_used": [], "jd_keywords_incorporated": []}
        
        parsed = self.parse_json_response(response)
        
        if not parsed:
            logger.error("❌ Failed to parse summary JSON")
            return {"summary": "", "key_metrics_used": [], "jd_keywords_incorporated": []}
        
        logger.info(f"✅ Generated JD-specific summary with {len(parsed.get('key_metrics_used', []))} real metrics")
        
        return parsed
    
    def _generate_experience_bullets(
        self, 
        resume_text: str, 
        job_description: str, 
        missing_keywords: List[str],
        cv_analysis: Dict
    ) -> List[Dict]:
        """
        Generate experience bullets mapped to actual CV companies/roles
        """
        companies = cv_analysis.get('companies', [])
        
        if not companies:
            logger.warning("⚠️ No companies found in CV, generating generic bullets")
            return self._generate_generic_bullets(missing_keywords)
        
        # Map each missing keyword to best-fit company
        companies_json = json.dumps(companies, indent=2)
        keywords_str = ', '.join(missing_keywords[:10])
        
        prompt = f"""You are a resume optimization expert. Map missing keywords to actual CV experience and generate contextual bullets.

Job Description Requirements (extract missing skills):
{job_description[:1500]}

Missing Keywords to Add: {keywords_str}

Candidate's Work Experience:
{companies_json}

For each missing keyword, determine:
1. Which company/role best fits this keyword
2. Generate a STAR-format bullet that:
   - Uses the REAL company name and role
   - Incorporates the missing keyword naturally
   - Includes specific metrics if available
   - Sounds authentic to that company context

Return ONLY valid JSON array (max 8 bullets):
[
    {{
        "company": "Company X",
        "role": "Senior Data Scientist",
        "keyword_added": "Model supervision",
        "bullet": "Implemented model supervision framework for 12+ production ML models, reducing deployment errors by 35% and ensuring consistent performance monitoring across analytics solutions",
        "why_this_company": "Best fit because role involves ML deployment and production systems",
        "impact_metric": "35% reduction in deployment errors"
    }},
    {{
        "company": "Company Y",
        "role": "Data Analyst",
        "keyword_added": "Analytics framework",
        "bullet": "Developed and optimized analytics framework using Python and R, enabling data-driven decision-making for cross-functional teams and improving reporting efficiency by 50%",
        "why_this_company": "Early career role - good for foundational framework work",
        "impact_metric": "50% efficiency improvement"
    }}
]

CRITICAL RULES:
1. Use ONLY companies/roles from the candidate's actual CV
2. Include real or realistic metrics (%, numbers, time)
3. Match keyword context to company context
4. Don't place "model supervision" at a junior analyst role
5. Make it sound authentic - not generic
6. Use action verbs: Implemented, Developed, Optimized, Led
"""
        
        response = self.generate(prompt, temperature=0.4)
        
        if not response:
            logger.error("❌ Failed to generate experience bullets")
            return self._generate_generic_bullets(missing_keywords)
        
        parsed = self.parse_json_response(response)
        
        if not parsed or not isinstance(parsed, list):
            logger.error("❌ Failed to parse experience bullets JSON")
            return self._generate_generic_bullets(missing_keywords)
        
        logger.info(f"✅ Generated {len(parsed)} experience bullets mapped to actual companies")
        
        return parsed
    
    def _generate_skills_suggestions(
        self, 
        resume_text: str, 
        job_description: str,
        missing_keywords: List[str]
    ) -> Dict:
        """
        Suggest keywords for Skills section
        """
        prompt = f"""Analyze this JD and suggest keywords for the "Skills" or "Technical Skills" section of a resume.

Job Description:
{job_description[:1500]}

Missing Keywords: {', '.join(missing_keywords[:15])}

Current Resume:
{resume_text[:2000]}

Return ONLY valid JSON:
{{
    "hard_skills_to_add": [
        {{"skill": "R Programming", "importance": 95, "jd_mentions": 3}},
        {{"skill": "Statistical Modeling", "importance": 90, "jd_mentions": 2}}
    ],
    "soft_skills_to_add": [
        {{"skill": "Cross-functional Collaboration", "importance": 75}},
        {{"skill": "Stakeholder Communication", "importance": 70}}
    ],
    "tools_to_add": [
        {{"skill": "Tableau", "importance": 80}},
        {{"skill": "Git", "importance": 75}}
    ],
    "recommended_skills_section": "Python • R • SQL • Machine Learning • Statistical Modeling • Deep Learning • TensorFlow • PyTorch • Data Visualization • Tableau • Git • AWS • Docker • Model Deployment"
}}

Focus on:
1. Technical skills mentioned in JD
2. Industry-standard tools for this role
3. Skills that fit the seniority level
4. Skills candidate likely has but didn't list
"""
        
        response = self.generate(prompt, temperature=0.3)
        
        if not response:
            logger.error("❌ Failed to generate skills suggestions")
            return self._get_default_skills()
        
        parsed = self.parse_json_response(response)
        
        if not parsed:
            logger.error("❌ Failed to parse skills suggestions JSON")
            return self._get_default_skills()
        
        logger.info(f"✅ Suggested {len(parsed.get('hard_skills_to_add', []))} hard skills, "
                   f"{len(parsed.get('tools_to_add', []))} tools")
        
        return parsed
    
    def _generate_generic_bullets(self, missing_keywords: List[str]) -> List[Dict]:
        """Fallback generic bullets if CV parsing fails"""
        bullets = []
        for keyword in missing_keywords[:5]:
            bullets.append({
                "company": "Your relevant role",
                "role": "Position that used this skill",
                "keyword_added": keyword,
                "bullet": f"Utilized {keyword} to develop and implement solutions that improved system performance and efficiency, resulting in measurable business impact",
                "why_this_company": "Determine best fit from your experience",
                "impact_metric": "Add specific metric from your work"
            })
        return bullets
    
    def _get_default_cv_structure(self) -> Dict:
        """Fallback CV structure"""
        return {
            "current_role": "Professional",
            "years_experience": 0,
            "companies": [],
            "quantified_achievements": [],
            "education": {},
            "current_skills": []
        }
    
    def _get_default_skills(self) -> Dict:
        """Fallback skills suggestions"""
        return {
            "hard_skills_to_add": [],
            "soft_skills_to_add": [],
            "tools_to_add": [],
            "recommended_skills_section": ""
        }
