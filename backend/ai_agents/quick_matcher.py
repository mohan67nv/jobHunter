"""
Quick Matcher - Fast keyword-based matching for real-time scoring
Lightweight alternative to full AI analysis for initial job filtering
"""
import re
from typing import Dict, List, Set
from utils.logger import setup_logger

logger = setup_logger(__name__)


class QuickMatcher:
    """Fast keyword-based matcher for real-time job scoring"""
    
    def __init__(self):
        self.logger = logger
    
    def calculate_quick_match(self, resume_text: str, job_description: str, job_title: str = "") -> float:
        """
        Calculate quick match score based on keyword overlap
        
        Fast algorithm (~0.1 seconds) for real-time matching
        Returns score 0-100 based on:
        - Keyword overlap (50%)
        - Required skills match (30%)
        - Job title relevance (20%)
        
        Args:
            resume_text: User's resume text
            job_description: Job description text
            job_title: Job title for additional matching
            
        Returns:
            Match score 0-100
        """
        try:
            # Extract keywords and skills
            resume_keywords = self._extract_keywords(resume_text.lower())
            job_keywords = self._extract_keywords(job_description.lower())
            
            # Extract technical skills specifically
            resume_skills = self._extract_technical_skills(resume_text.lower())
            job_skills = self._extract_technical_skills(job_description.lower())
            
            # Calculate overlaps
            keyword_overlap = len(resume_keywords & job_keywords) / max(len(job_keywords), 1)
            skill_overlap = len(resume_skills & job_skills) / max(len(job_skills), 1)
            
            # Job title match
            title_score = self._calculate_title_match(resume_text.lower(), job_title.lower())
            
            # Weighted score
            match_score = (
                keyword_overlap * 50 +  # General keywords
                skill_overlap * 30 +     # Technical skills
                title_score * 20          # Title relevance
            )
            
            return min(100, max(0, match_score))
            
        except Exception as e:
            self.logger.error(f"Error in quick match: {e}")
            return 0
    
    def _extract_keywords(self, text: str) -> Set[str]:
        """Extract important keywords from text"""
        # Common stopwords to ignore
        stopwords = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
            'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'should',
            'could', 'can', 'may', 'might', 'must', 'this', 'that', 'these', 'those'
        }
        
        # Extract words (2+ characters)
        words = re.findall(r'\b[a-z]{2,}\b', text)
        
        # Filter stopwords and get unique keywords
        keywords = {w for w in words if w not in stopwords and len(w) > 2}
        
        return keywords
    
    def _extract_technical_skills(self, text: str) -> Set[str]:
        """Extract technical skills and tools"""
        # Common technical skills/tools (can be expanded)
        skill_patterns = [
            # Programming languages
            r'\b(python|java|javascript|typescript|c\+\+|c#|go|rust|ruby|php|swift|kotlin)\b',
            # Data Science / ML
            r'\b(pytorch|tensorflow|keras|scikit-learn|pandas|numpy|spark|hadoop|kafka)\b',
            # Cloud / DevOps
            r'\b(aws|azure|gcp|docker|kubernetes|jenkins|terraform|ansible|gitlab|github)\b',
            # Databases
            r'\b(sql|mysql|postgresql|mongodb|redis|elasticsearch|cassandra)\b',
            # Frameworks
            r'\b(react|angular|vue|django|flask|fastapi|spring|node\.?js|express)\b',
            # Methods
            r'\b(agile|scrum|devops|ci/cd|mlops|rest|graphql|microservices)\b',
            # ML specific
            r'\b(machine learning|deep learning|nlp|computer vision|reinforcement learning)\b',
            r'\b(neural network|cnn|rnn|lstm|transformer|bert|gpt)\b',
        ]
        
        skills = set()
        for pattern in skill_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            skills.update([m.lower() for m in matches])
        
        return skills
    
    def _calculate_title_match(self, resume_text: str, job_title: str) -> float:
        """Calculate how well resume matches job title"""
        if not job_title:
            return 0.5  # Neutral score if no title
        
        # Extract key terms from job title
        title_terms = set(re.findall(r'\b[a-z]{3,}\b', job_title.lower()))
        
        # Remove common words
        title_terms = {t for t in title_terms if t not in {'the', 'and', 'or', 'senior', 'junior', 'lead'}}
        
        if not title_terms:
            return 0.5
        
        # Check how many title terms appear in resume
        found_terms = sum(1 for term in title_terms if term in resume_text)
        
        return found_terms / len(title_terms)
    
    def batch_calculate(self, resume_text: str, jobs: List[Dict]) -> Dict[int, float]:
        """
        Calculate quick match for multiple jobs efficiently
        
        Args:
            resume_text: User's resume
            jobs: List of job dicts with 'id', 'description', 'title'
            
        Returns:
            Dict mapping job_id to match_score
        """
        results = {}
        
        for job in jobs:
            job_id = job.get('id')
            description = job.get('description', '')
            title = job.get('title', '')
            
            if job_id and description:
                score = self.calculate_quick_match(resume_text, description, title)
                results[job_id] = score
        
        return results
