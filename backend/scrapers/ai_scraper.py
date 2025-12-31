"""
AI-Powered Job Scraper - Uses DeepSeek to search and extract job listings
Bypasses anti-scraping by using AI to search the web and extract structured job data
"""
from typing import List, Dict, Optional
from datetime import datetime
import json
import re
from scrapers.base_scraper import BaseScraper
from ai_agents.model_config import get_model_config

# Import AI clients
try:
    from openai import OpenAI
    import os
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


class AIJobScraper(BaseScraper):
    """AI-powered scraper using DeepSeek to extract job listings"""
    
    def __init__(self, provider: str = 'deepseek'):
        """
        Initialize scraper
        
        Args:
            provider: AI provider (uses model_config.py settings)
        """
        super().__init__()
        
        if not OPENAI_AVAILABLE:
            self.logger.error("❌ OpenAI library not installed")
            return
        
        # Get model config for AIJobScraper
        config = get_model_config("AIJobScraper")
        self.provider = config["provider"]
        self.model = config["model"]
        
        # Initialize AI client
        if self.provider == "deepseek":
            api_key = os.getenv('DEEPSEEK_API_KEY')
            if not api_key:
                self.logger.error("❌ DEEPSEEK_API_KEY not set")
                return
            self.client = OpenAI(
                api_key=api_key,
                base_url="https://api.deepseek.com"
            )
        else:
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                self.logger.error("❌ OPENAI_API_KEY not set")
                return
            self.client = OpenAI(api_key=api_key)
        
        self.logger.info(f"✅ AI Scraper initialized with {self.provider} ({self.model})")
    
    def scrape(self, keyword: str, location: str = "Germany", 
               site: str = "indeed.de", max_results: int = 20) -> List[Dict]:
        """
        Use AI to search and extract job listings from a specific site
        
        Args:
            keyword: Job search keyword
            location: Location to search
            site: Target job site (indeed.de, stepstone.de, glassdoor.com, etc.)
            max_results: Maximum number of jobs to extract
            
        Returns:
            List of normalized job dictionaries
        """
        if not OPENAI_AVAILABLE or not hasattr(self, 'client'):
            self.logger.error("❌ AI client not available")
            return []
        
        self.logger.info(f"🤖 AI scraping {site} for '{keyword}' in '{location}'...")
        
        try:
            # Create AI prompt to search and extract jobs
            prompt = self._create_search_prompt(keyword, location, site, max_results)
            
            # Call AI to search and extract
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a job search assistant. Search the web for job listings and extract structured data. Return valid JSON only."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.1,
                max_tokens=4000
            )
            
            # Parse AI response
            content = response.choices[0].message.content
            jobs = self._parse_ai_response(content, site)
            
            self.logger.info(f"  ✅ {site}: {len(jobs)} jobs extracted by AI")
            self.log_scraping_stats(jobs)
            
            return jobs
        
        except Exception as e:
            self.logger.error(f"  ❌ {site}: AI scraping error - {e}")
            return []
    
    def _create_search_prompt(self, keyword: str, location: str, 
                            site: str, max_results: int) -> str:
        """Create AI prompt for job extraction"""
        
        return f"""Search {site} for job listings matching these criteria:
- Job Title/Keywords: {keyword}
- Location: {location}
- Number of results: {max_results}

Extract REAL, CURRENT job listings from {site}. For each job, extract:
1. title (job title)
2. company (company name)
3. location (job location)
4. url (direct link to job posting)
5. description (job description, 200-500 chars)
6. posted_date (when posted, e.g., "2 days ago")
7. salary (if available)
8. job_type (full-time, part-time, contract, etc.)

IMPORTANT:
- Search the REAL {site} website
- Extract ACTUAL current job listings (not examples)
- Include direct URLs to real job postings
- Return ONLY valid JSON array format
- Each job must have title, company, location, and url
- Maximum {max_results} jobs

Return format:
[
  {{
    "title": "Senior Machine Learning Engineer",
    "company": "Example GmbH",
    "location": "Berlin, Germany",
    "url": "https://{site}/job/12345",
    "description": "We are looking for...",
    "posted_date": "2 days ago",
    "salary": "€70,000 - €90,000",
    "job_type": "full-time"
  }}
]

Return ONLY the JSON array, no other text."""
    
    def _parse_ai_response(self, content: str, site: str) -> List[Dict]:
        """Parse AI response and normalize to job format"""
        jobs = []
        
        try:
            # Extract JSON from response
            json_match = re.search(r'\[\s*\{.*\}\s*\]', content, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                jobs_data = json.loads(json_str)
            else:
                # Try parsing entire content as JSON
                jobs_data = json.loads(content)
            
            # Normalize each job
            for job_data in jobs_data:
                try:
                    # Parse posted date
                    posted_str = job_data.get('posted_date', '')
                    posted_date = self._parse_relative_date(posted_str)
                    
                    raw_job = {
                        "title": job_data.get('title', ''),
                        "company": job_data.get('company', ''),
                        "location": job_data.get('location', ''),
                        "url": job_data.get('url', ''),
                        "description": job_data.get('description', ''),
                        "posted_date": posted_date,
                        "salary": job_data.get('salary'),
                        "job_type": job_data.get('job_type'),
                        "requirements": None,
                        "benefits": None,
                    }
                    
                    # Normalize and set source
                    normalized = self.normalize_job(raw_job)
                    
                    # Extract source from site domain
                    if 'indeed' in site.lower():
                        normalized["source"] = "Indeed"
                    elif 'stepstone' in site.lower():
                        normalized["source"] = "StepStone"
                    elif 'glassdoor' in site.lower():
                        normalized["source"] = "Glassdoor"
                    elif 'monster' in site.lower():
                        normalized["source"] = "Monster"
                    elif 'arbeitsagentur' in site.lower():
                        normalized["source"] = "Arbeitsagentur"
                    else:
                        normalized["source"] = site.split('.')[0].title()
                    
                    if self.validate_job(normalized):
                        jobs.append(normalized)
                
                except Exception as e:
                    self.logger.warning(f"Error parsing job from AI response: {e}")
                    continue
        
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse AI response as JSON: {e}")
            self.logger.debug(f"AI Response: {content[:500]}")
        
        return jobs
    
    def _parse_relative_date(self, date_str: str) -> datetime:
        """Parse relative date strings like '2 days ago' to datetime"""
        now = datetime.now()
        
        if not date_str:
            return now
        
        date_str = date_str.lower()
        
        # Today
        if 'today' in date_str or 'just now' in date_str:
            return now
        
        # Days ago
        days_match = re.search(r'(\d+)\s*day', date_str)
        if days_match:
            days = int(days_match.group(1))
            from datetime import timedelta
            return now - timedelta(days=days)
        
        # Weeks ago
        weeks_match = re.search(r'(\d+)\s*week', date_str)
        if weeks_match:
            weeks = int(weeks_match.group(1))
            from datetime import timedelta
            return now - timedelta(weeks=weeks)
        
        # Months ago
        months_match = re.search(r'(\d+)\s*month', date_str)
        if months_match:
            months = int(months_match.group(1))
            from datetime import timedelta
            return now - timedelta(days=months * 30)
        
        return now


# Specific site scrapers using AI
class AIIndeedScraper(AIJobScraper):
    """AI-powered Indeed scraper"""
    def scrape(self, keyword: str, location: str = "Germany", **kwargs) -> List[Dict]:
        return super().scrape(keyword, location, site="indeed.de", max_results=20)


class AIStepStoneScraper(AIJobScraper):
    """AI-powered StepStone scraper"""
    def scrape(self, keyword: str, location: str = "Germany", **kwargs) -> List[Dict]:
        return super().scrape(keyword, location, site="stepstone.de", max_results=20)


class AIGlassdoorScraper(AIJobScraper):
    """AI-powered Glassdoor scraper"""
    def scrape(self, keyword: str, location: str = "Germany", **kwargs) -> List[Dict]:
        return super().scrape(keyword, location, site="glassdoor.com", max_results=20)


class AIMonsterScraper(AIJobScraper):
    """AI-powered Monster scraper"""
    def scrape(self, keyword: str, location: str = "Germany", **kwargs) -> List[Dict]:
        return super().scrape(keyword, location, site="monster.de", max_results=20)
