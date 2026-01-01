"""
Real Industry-Standard ATS Scorer
Uses actual ATS algorithms: keyword matching, density, format checks
NO AI - pure rules-based scoring like Workday, Greenhouse, Taleo
"""
import re
from typing import Dict, List, Set
from collections import Counter
from utils.logger import setup_logger

logger = setup_logger(__name__)


class RealATSScorer:
    """
    Industry-standard ATS scoring using actual ATS algorithms
    - Exact keyword matching
    - Keyword density calculation
    - Format quality checks
    - Hard requirement filters
    - Mathematical scoring (not AI guessing)
    """
    
    def __init__(self):
        logger.info("✅ RealATSScorer initialized (rules-based, no AI)")
    
    def score(self, resume_text: str, job_description: str, jd_keywords: Dict = None) -> Dict:
        """
        Calculate ATS score using industry-standard rules
        
        Returns:
            {
                "ats_score": 75,
                "keyword_score": 80,
                "format_score": 70,
                "exact_matches": 15,
                "total_keywords": 20,
                "match_rate": 75.0,
                "keyword_density": {...},
                "hard_filters": {...},
                "breakdown": {...}
            }
        """
        # Step 1: Extract keywords from JD
        jd_keyword_list = self._extract_jd_keywords(job_description, jd_keywords)
        
        # Step 2: Count exact matches in resume
        exact_matches = self._count_exact_matches(resume_text, jd_keyword_list)
        
        # Step 3: Calculate keyword density
        keyword_density = self._calculate_keyword_density(resume_text, exact_matches)
        
        # Step 4: Check format quality
        format_score = self._check_format_quality(resume_text)
        
        # Step 5: Apply hard filters
        hard_filters = self._apply_hard_filters(resume_text, job_description)
        
        # Step 6: Calculate final score
        keyword_score = self._calculate_keyword_score(exact_matches, jd_keyword_list)
        final_score = self._calculate_final_score(keyword_score, format_score, hard_filters)
        
        # Get resume stats
        resume_stats = self._get_resume_stats(resume_text)
        
        logger.info(f"✅ Real ATS Score: {final_score}% (Keywords: {keyword_score}%, Format: {format_score}%)")
        logger.info(f"   Exact matches: {exact_matches['total_matched']}/{len(jd_keyword_list)} keywords")
        
        return {
            "ats_score": final_score,
            "keyword_score": keyword_score,
            "format_score": format_score,
            "exact_matches": exact_matches['total_matched'],
            "total_keywords": len(jd_keyword_list),
            "match_rate": round((exact_matches['total_matched'] / len(jd_keyword_list) * 100) if jd_keyword_list else 0, 1),
            "keyword_density": keyword_density,
            "hard_filters": hard_filters,
            "matched_keywords": exact_matches['matched'],
            "missing_keywords": exact_matches['missing'],
            "resume_stats": resume_stats,
            "scoring_method": "Rules-based (exact keyword matching + format checks)",
            "breakdown": {
                "keyword_weight": "70%",
                "format_weight": "30%",
                "formula": f"({keyword_score}% × 0.7) + ({format_score}% × 0.3) = {final_score}%"
            }
        }
    
    def _extract_jd_keywords(self, job_description: str, jd_keywords: Dict = None) -> List[str]:
        """Extract keywords from JD (use AI-extracted if available, else extract manually)"""
        keywords = []
        
        # Use AI-extracted keywords if available
        if jd_keywords:
            for category, kw_list in jd_keywords.items():
                if category == 'ats_critical_phrases':
                    keywords.extend(jd_keywords.get('ats_critical_phrases', []))
                elif isinstance(kw_list, list):
                    for item in kw_list:
                        if isinstance(item, dict) and 'keyword' in item:
                            keywords.append(item['keyword'])
                            # Add variations
                            if 'variations' in item:
                                keywords.extend(item.get('variations', []))
        
        # Manual extraction as fallback
        if not keywords:
            keywords = self._manual_keyword_extraction(job_description)
        
        # Remove duplicates and clean
        keywords = list(set([kw.strip().lower() for kw in keywords if kw.strip()]))
        
        logger.info(f"📊 Extracted {len(keywords)} unique keywords from JD")
        
        return keywords
    
    def _manual_keyword_extraction(self, job_description: str) -> List[str]:
        """Manual keyword extraction (fallback)"""
        keywords = []
        
        # Common technical terms patterns
        tech_patterns = [
            r'\b(?:Python|Java|JavaScript|C\+\+|SQL|R|Ruby|PHP|Swift|Kotlin)\b',
            r'\b(?:Machine Learning|ML|Deep Learning|AI|Data Science|NLP|Computer Vision)\b',
            r'\b(?:AWS|Azure|GCP|Docker|Kubernetes|Git|CI/CD)\b',
            r'\b(?:React|Angular|Vue|Node\.js|Django|Flask|Spring)\b',
            r'\b(?:TensorFlow|PyTorch|Scikit-learn|Pandas|NumPy)\b',
        ]
        
        for pattern in tech_patterns:
            matches = re.finditer(pattern, job_description, re.IGNORECASE)
            keywords.extend([m.group() for m in matches])
        
        # Extract multi-word phrases (important skills)
        phrases = re.findall(r'\b(?:[A-Z][a-z]+(?: [A-Z][a-z]+)*)\b', job_description)
        keywords.extend([p for p in phrases if len(p.split()) >= 2 and len(p.split()) <= 4])
        
        return keywords
    
    def _count_exact_matches(self, resume_text: str, keywords: List[str]) -> Dict:
        """Count exact keyword matches (case-insensitive)"""
        resume_lower = resume_text.lower()
        
        matched = []
        missing = []
        keyword_counts = {}
        
        for keyword in keywords:
            keyword_lower = keyword.lower()
            
            # Count occurrences
            count = len(re.findall(r'\b' + re.escape(keyword_lower) + r'\b', resume_lower))
            
            if count > 0:
                matched.append(keyword)
                keyword_counts[keyword] = count
            else:
                missing.append(keyword)
        
        return {
            "total_matched": len(matched),
            "total_missing": len(missing),
            "matched": matched,
            "missing": missing,
            "keyword_counts": keyword_counts
        }
    
    def _calculate_keyword_density(self, resume_text: str, exact_matches: Dict) -> Dict:
        """Calculate keyword density (how often keywords appear)"""
        total_words = len(resume_text.split())
        keyword_counts = exact_matches['keyword_counts']
        
        densities = {}
        for keyword, count in keyword_counts.items():
            density = (count / total_words * 100) if total_words > 0 else 0
            densities[keyword] = {
                "count": count,
                "density_percent": round(density, 2),
                "quality": "Excellent" if count >= 3 else ("Good" if count == 2 else "Weak")
            }
        
        return {
            "total_resume_words": total_words,
            "keyword_densities": densities,
            "average_mentions": round(sum(keyword_counts.values()) / len(keyword_counts), 1) if keyword_counts else 0
        }
    
    def _check_format_quality(self, resume_text: str) -> int:
        """Check resume format quality (parsability)"""
        score = 100
        
        # Check 1: Has standard sections (10 points each)
        sections = ['experience', 'education', 'skills']
        for section in sections:
            if not re.search(section, resume_text, re.IGNORECASE):
                score -= 10
                logger.debug(f"   Missing section: {section} (-10 points)")
        
        # Check 2: Has bullet points (good formatting)
        if not re.search(r'[•\-\*]', resume_text):
            score -= 10
            logger.debug("   No bullet points found (-10 points)")
        
        # Check 3: Has dates (experience dates)
        if not re.search(r'\b(19|20)\d{2}\b', resume_text):
            score -= 10
            logger.debug("   No dates found (-10 points)")
        
        # Check 4: Reasonable length (500-2000 words)
        word_count = len(resume_text.split())
        if word_count < 500:
            score -= 15
            logger.debug(f"   Too short: {word_count} words (-15 points)")
        elif word_count > 2000:
            score -= 10
            logger.debug(f"   Too long: {word_count} words (-10 points)")
        
        # Check 5: Has contact info patterns
        if not re.search(r'[@\.]|phone|email', resume_text, re.IGNORECASE):
            score -= 10
            logger.debug("   No contact info detected (-10 points)")
        
        return max(0, score)
    
    def _apply_hard_filters(self, resume_text: str, job_description: str) -> Dict:
        """Apply hard requirement filters (pass/fail checks)"""
        filters = {
            "all_passed": True,
            "checks": []
        }
        
        # Check 1: Degree requirement
        if re.search(r"(?:master|phd|doctorate|msc|ma)", job_description, re.IGNORECASE):
            has_degree = bool(re.search(r"(?:master|phd|doctorate|msc|ma|m\.s\.|bachelor)", resume_text, re.IGNORECASE))
            filters["checks"].append({
                "filter": "Degree Requirement",
                "required": "Master's or PhD mentioned in JD",
                "status": "✓ Pass" if has_degree else "✗ Fail",
                "passed": has_degree
            })
            if not has_degree:
                filters["all_passed"] = False
        
        # Check 2: Years of experience
        exp_match = re.search(r"(\d+)\+?\s*(?:years?|yrs?)", job_description, re.IGNORECASE)
        if exp_match:
            required_years = int(exp_match.group(1))
            resume_years = re.findall(r"(\d+)\+?\s*(?:years?|yrs?)", resume_text, re.IGNORECASE)
            max_years = max([int(y) for y in resume_years], default=0)
            
            passed = max_years >= required_years
            filters["checks"].append({
                "filter": "Years of Experience",
                "required": f"{required_years}+ years",
                "found": f"{max_years} years",
                "status": "✓ Pass" if passed else "✗ Fail",
                "passed": passed
            })
            if not passed:
                filters["all_passed"] = False
        
        return filters
    
    def _calculate_keyword_score(self, exact_matches: Dict, jd_keywords: List[str]) -> int:
        """Calculate keyword match score (0-100)"""
        if not jd_keywords:
            return 0
        
        total_matched = exact_matches['total_matched']
        total_keywords = len(jd_keywords)
        
        # Base score: percentage of keywords matched
        base_score = (total_matched / total_keywords * 100) if total_keywords > 0 else 0
        
        # Bonus: keyword density (keywords mentioned multiple times)
        keyword_counts = exact_matches['keyword_counts']
        multi_mentions = sum(1 for count in keyword_counts.values() if count >= 2)
        density_bonus = min(10, multi_mentions * 2)  # Max +10 points for density
        
        final_score = min(100, base_score + density_bonus)
        
        return round(final_score)
    
    def _calculate_final_score(self, keyword_score: int, format_score: int, hard_filters: Dict) -> int:
        """Calculate final ATS score using industry weights"""
        # Industry standard: 70% keywords, 30% format
        final_score = (keyword_score * 0.7) + (format_score * 0.3)
        
        # Apply hard filter penalty
        if not hard_filters['all_passed']:
            # In real ATS, failing hard filters = auto-reject
            # We'll reduce score significantly but not zero
            final_score = final_score * 0.6  # 40% penalty
            logger.warning(f"⚠️ Hard filters failed - applying 40% penalty")
        
        return round(final_score)
    
    def _get_resume_stats(self, resume_text: str) -> Dict:
        """Get resume statistics"""
        words = resume_text.split()
        
        return {
            "total_words": len(words),
            "total_characters": len(resume_text),
            "total_lines": len(resume_text.split('\n')),
            "average_word_length": round(sum(len(w) for w in words) / len(words), 1) if words else 0
        }
