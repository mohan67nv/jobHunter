"""
Advanced ATS Keyword Analyzer
Uses DeepSeek Reasoner for deep JD analysis and strategic keyword extraction
"""
import json
from typing import Dict, List
from ai_agents.base_agent import BaseAgent
from utils.logger import setup_logger

logger = setup_logger(__name__)


class ATSKeywordAnalyzer(BaseAgent):
    """
    Deep ATS keyword analysis using DeepSeek Reasoner
    Extracts categorized keywords, identifies gaps, provides strategic recommendations
    """
    
    def __init__(self):
        # Use DeepSeek Reasoner for deep analysis
        super().__init__(preferred_provider="deepseek", model="deepseek-reasoner")
        logger.info("✅ ATSKeywordAnalyzer initialized with DeepSeek Reasoner")
    
    def analyze_jd_keywords(self, job_description: str) -> Dict:
        """
        Deep analysis of job description to extract ALL ATS-critical keywords
        
        Args:
            job_description: Full job description text
            
        Returns:
            Dict with categorized keywords, ATS importance scores, and context
        """
        prompt = f"""You are an expert ATS (Applicant Tracking System) keyword analyzer. Your job is to extract EVERY keyword that an ATS would scan for from this job description.

Job Description:
{job_description}

Analyze this JD deeply and extract keywords in these categories. Return ONLY valid JSON:

{{
    "high_priority_technical": [
        {{"keyword": "Python", "importance": 95, "context": "Programming language - explicitly required", "variations": ["python", "Python3"]}},
        {{"keyword": "Statistical analysis", "importance": 90, "context": "Core technical skill", "variations": ["statistics", "statistical methods"]}}
    ],
    "seniority_leadership": [
        {{"keyword": "Oversee", "importance": 85, "context": "Senior-level action verb indicating management responsibility", "variations": ["oversees", "overseeing", "oversight"]}},
        {{"keyword": "Manage", "importance": 85, "context": "Leadership keyword", "variations": ["manages", "managing", "management"]}}
    ],
    "qualifications_background": [
        {{"keyword": "Master's degree", "importance": 90, "context": "Educational requirement", "variations": ["MSc", "Masters", "Master of Science"]}},
        {{"keyword": "PhD", "importance": 85, "context": "Preferred education level", "variations": ["Doctorate", "Doctoral degree"]}}
    ],
    "industry_domain": [
        {{"keyword": "Data Science", "importance": 95, "context": "Core domain expertise", "variations": ["Data Scientist", "DS"]}},
        {{"keyword": "Analytics", "importance": 90, "context": "Domain terminology", "variations": ["analytical", "analytics solutions"]}}
    ],
    "soft_skills_cultural": [
        {{"keyword": "Results-oriented", "importance": 75, "context": "Cultural fit keyword", "variations": ["result-driven", "outcome-focused"]}},
        {{"keyword": "Business-focused", "importance": 80, "context": "Strategic mindset", "variations": ["business-oriented", "business value"]}}
    ],
    "tools_technologies": [
        {{"keyword": "R", "importance": 90, "context": "Required programming language", "variations": ["R language", "R programming"]}},
        {{"keyword": "Python", "importance": 95, "context": "Required programming language", "variations": ["Python3", "python"]}}
    ],
    "action_verbs": [
        {{"keyword": "Implement", "importance": 80, "context": "Action verb showing execution capability", "variations": ["implementation", "implementing"]}},
        {{"keyword": "Optimize", "importance": 85, "context": "Performance improvement focus", "variations": ["optimization", "optimizing"]}}
    ],
    "company_specific": [
        {{"keyword": "Hays", "importance": 70, "context": "Company name - helps with ATS matching", "variations": ["Hays Professional Solutions"]}},
        {{"keyword": "Reference number: 743926/1", "importance": 95, "context": "CRITICAL - Recruiters search by reference number", "variations": ["743926", "Ref: 743926/1"]}}
    ],
    "ats_critical_phrases": [
        "Analytics solutions",
        "Model supervision",
        "Informed decision-making",
        "Quantitative discipline",
        "Data reviews",
        "Analytics framework",
        "Data management operations",
        "Complex challenges"
    ]
}}

INSTRUCTIONS:
1. Read EVERY sentence carefully
2. Extract exact phrases from the JD (don't paraphrase)
3. Identify implicit requirements (if JD says "oversee", ATS looks for leadership)
4. Include reference numbers, company names, location details
5. Rate importance 0-100 (100 = must-have for ATS to rank resume high)
6. Provide context explaining WHY this keyword matters for ATS
7. List variations/synonyms the ATS might search for

Focus on keywords that an ATS would use to FILTER and RANK candidates. Think like a recruiter setting up search filters.
"""
        
        response = self.generate(prompt, temperature=0.3)
        
        if not response:
            logger.error("❌ Failed to get response from DeepSeek Reasoner")
            return self._get_default_keywords()
        
        parsed = self.parse_json_response(response)
        
        if not parsed:
            logger.error("❌ Failed to parse keyword analysis JSON")
            return self._get_default_keywords()
        
        logger.info(f"✅ Extracted keywords: {len(parsed.get('high_priority_technical', []))} technical, "
                   f"{len(parsed.get('seniority_leadership', []))} leadership, "
                   f"{len(parsed.get('tools_technologies', []))} tools")
        
        return parsed
    
    def analyze_cv_gaps(self, resume_text: str, jd_keywords: Dict) -> Dict:
        """
        Identify missing keywords and provide strategic recommendations
        
        Args:
            resume_text: Full resume text
            jd_keywords: Extracted keywords from JD
            
        Returns:
            Gap analysis with missing keywords, under-emphasized areas, and recommendations
        """
        # Flatten all keywords for analysis
        all_jd_keywords = []
        for category, keywords in jd_keywords.items():
            if category != 'ats_critical_phrases':
                for kw in keywords:
                    all_jd_keywords.append({
                        'keyword': kw['keyword'],
                        'importance': kw['importance'],
                        'category': category,
                        'context': kw['context']
                    })
        
        keywords_json = json.dumps(all_jd_keywords, indent=2)
        
        prompt = f"""You are an expert resume optimizer. Compare this resume against ATS keywords and identify gaps.

Resume:
{resume_text[:4000]}

ATS Keywords to Check:
{keywords_json}

Critical Phrases:
{', '.join(jd_keywords.get('ats_critical_phrases', []))}

Analyze and return ONLY valid JSON:

{{
    "current_ats_score": 75,
    "missing_critical": [
        {{
            "keyword": "Model supervision",
            "importance": 90,
            "category": "high_priority_technical",
            "why_missing": "Resume mentions 'MLOps pipelines' but not explicit 'model supervision' phrase",
            "recommendation": "Change 'MLOps pipelines' to 'Model supervision and MLOps pipelines in production'",
            "where_to_add": "Experience section - current role description",
            "impact": "+15 ATS points"
        }}
    ],
    "under_emphasized": [
        {{
            "keyword": "Results-oriented",
            "current_mentions": 0,
            "should_mention": 2,
            "category": "soft_skills_cultural",
            "recommendation": "Add 'Results-oriented Data Scientist' to professional summary",
            "impact": "+5 ATS points"
        }}
    ],
    "well_covered": [
        "Python",
        "Machine Learning",
        "SQL",
        "Data Analysis"
    ],
    "strategic_improvements": [
        {{
            "section": "Professional Summary",
            "current_issue": "Too developer-heavy, not enough 'Data Scientist' terminology",
            "fix": "Rewrite to include: 'quantitative discipline', 'analytics solutions', 'business-focused'",
            "example": "Senior Data Scientist with MSc in quantitative discipline and 4+ years implementing business-focused analytics solutions...",
            "impact": "+10 ATS points"
        }},
        {{
            "section": "Job Title Reference",
            "current_issue": "Missing reference number that recruiters search for",
            "fix": "Add 'Ref: 743926/1' under your name or in header",
            "impact": "+20 ATS points (CRITICAL for recruiter searches)"
        }}
    ],
    "keyword_placement_guide": [
        {{
            "keyword": "Analytics solutions",
            "current_usage": "Not found",
            "optimal_frequency": 2,
            "where": ["Professional summary", "Experience bullets"],
            "how": "Replace generic terms like 'ML systems' with 'analytics solutions'"
        }}
    ],
    "estimated_score_after_fixes": 92,
    "priority_actions": [
        "1. Add reference number Ref: 743926/1 to header (+20 points)",
        "2. Rewrite summary with 'quantitative discipline', 'analytics solutions' (+10 points)",
        "3. Change 'MLOps' to 'Model supervision in production' (+15 points)",
        "4. Add 'R language' to skills if you have any R experience (+10 points)"
    ]
}}

Be specific with line-by-line recommendations. Show exact text to replace and why.
"""
        
        response = self.generate(prompt, temperature=0.4)
        
        if not response:
            logger.error("❌ Failed to get gap analysis")
            return self._get_default_gaps()
        
        parsed = self.parse_json_response(response)
        
        if not parsed:
            logger.error("❌ Failed to parse gap analysis JSON")
            return self._get_default_gaps()
        
        logger.info(f"✅ Gap analysis: {len(parsed.get('missing_critical', []))} critical gaps, "
                   f"{len(parsed.get('strategic_improvements', []))} strategic improvements")
        
        return parsed
    
    def generate_comparison_table(self, jd_keywords: Dict, gap_analysis: Dict) -> List[Dict]:
        """
        Generate side-by-side comparison table for UI display
        
        Returns list of rows for visual comparison table
        """
        comparison = []
        
        # Get well covered keywords
        well_covered = set(gap_analysis.get('well_covered', []))
        
        # Get missing/under-emphasized
        missing_map = {item['keyword']: item for item in gap_analysis.get('missing_critical', [])}
        under_map = {item['keyword']: item for item in gap_analysis.get('under_emphasized', [])}
        
        # Process all categories
        for category, keywords in jd_keywords.items():
            if category == 'ats_critical_phrases':
                continue
                
            for kw_obj in keywords:
                keyword = kw_obj['keyword']
                status = "✅ Found" if keyword in well_covered else ("❌ Missing" if keyword in missing_map else "⚠️ Under-emphasized")
                
                action = ""
                if keyword in missing_map:
                    action = missing_map[keyword]['recommendation']
                elif keyword in under_map:
                    action = under_map[keyword]['recommendation']
                else:
                    action = "Good coverage - no action needed"
                
                comparison.append({
                    'jd_requirement': keyword,
                    'importance': kw_obj['importance'],
                    'category': category,
                    'resume_status': status,
                    'action_needed': action
                })
        
        # Sort by importance
        comparison.sort(key=lambda x: x['importance'], reverse=True)
        
        return comparison
    
    def _get_default_keywords(self) -> Dict:
        """Fallback when AI fails"""
        return {
            "high_priority_technical": [],
            "seniority_leadership": [],
            "qualifications_background": [],
            "industry_domain": [],
            "soft_skills_cultural": [],
            "tools_technologies": [],
            "action_verbs": [],
            "company_specific": [],
            "ats_critical_phrases": []
        }
    
    def _get_default_gaps(self) -> Dict:
        """Fallback gap analysis"""
        return {
            "current_ats_score": 50,
            "missing_critical": [],
            "under_emphasized": [],
            "well_covered": [],
            "strategic_improvements": [],
            "keyword_placement_guide": [],
            "estimated_score_after_fixes": 50,
            "priority_actions": []
        }
