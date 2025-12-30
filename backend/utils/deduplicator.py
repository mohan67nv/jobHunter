"""
Job deduplication engine
Uses fuzzy matching to identify duplicate job postings
"""
from typing import List, Tuple
from sqlalchemy.orm import Session
from models.job import Job
from utils.logger import setup_logger

try:
    from rapidfuzz import fuzz
    RAPIDFUZZ_AVAILABLE = True
except ImportError:
    RAPIDFUZZ_AVAILABLE = False

logger = setup_logger(__name__)


class Deduplicator:
    """Identifies and marks duplicate job postings"""
    
    def __init__(self, db: Session, similarity_threshold: int = 85):
        """
        Initialize deduplicator
        
        Args:
            db: Database session
            similarity_threshold: Minimum similarity score (0-100) to consider duplicate
        """
        self.db = db
        self.similarity_threshold = similarity_threshold
        
        if not RAPIDFUZZ_AVAILABLE:
            logger.warning("⚠️  RapidFuzz not installed. Using basic matching.")
    
    def deduplicate_all(self) -> List[Tuple[int, int]]:
        """
        Find and mark all duplicate jobs
        
        Returns:
            List of tuples (duplicate_id, original_id)
        """
        logger.info("🔍 Running deduplication on all active jobs...")
        
        # Get all active, non-duplicate jobs
        jobs = self.db.query(Job).filter(
            Job.is_active == True,
            Job.is_duplicate == False
        ).all()
        
        logger.info(f"Checking {len(jobs)} jobs for duplicates...")
        
        duplicates = []
        checked = set()
        
        for i, job1 in enumerate(jobs):
            if job1.id in checked:
                continue
            
            for job2 in jobs[i+1:]:
                if job2.id in checked:
                    continue
                
                if self._is_duplicate(job1, job2):
                    # Keep the older one (earliest posted_date) as original
                    if job1.posted_date <= job2.posted_date:
                        original = job1
                        duplicate = job2
                    else:
                        original = job2
                        duplicate = job1
                    
                    # Mark as duplicate
                    duplicate.is_duplicate = True
                    duplicate.duplicate_of = original.id
                    checked.add(duplicate.id)
                    
                    duplicates.append((duplicate.id, original.id))
                    logger.debug(f"Duplicate found: Job {duplicate.id} → {original.id}")
        
        # Commit changes
        try:
            self.db.commit()
            logger.info(f"✅ Marked {len(duplicates)} duplicates")
        except Exception as e:
            logger.error(f"Error committing duplicates: {e}")
            self.db.rollback()
        
        return duplicates
    
    def _is_duplicate(self, job1: Job, job2: Job) -> bool:
        """
        Check if two jobs are duplicates using fuzzy matching
        
        Args:
            job1: First job
            job2: Second job
            
        Returns:
            True if jobs are duplicates
        """
        # Must be from different sources (same source shouldn't have duplicates)
        if job1.source == job2.source:
            return False
        
        # Exact URL match (rare but possible)
        if job1.url == job2.url:
            return True
        
        # Combine title, company, and location for comparison
        str1 = f"{job1.title} {job1.company} {job1.location}".lower()
        str2 = f"{job2.title} {job2.company} {job2.location}".lower()
        
        if RAPIDFUZZ_AVAILABLE:
            # Use RapidFuzz for fuzzy matching
            similarity = fuzz.ratio(str1, str2)
        else:
            # Fallback to simple string matching
            similarity = self._simple_similarity(str1, str2)
        
        return similarity >= self.similarity_threshold
    
    def _simple_similarity(self, str1: str, str2: str) -> float:
        """
        Simple similarity calculation (fallback)
        
        Args:
            str1: First string
            str2: Second string
            
        Returns:
            Similarity score (0-100)
        """
        # Convert to sets of words
        words1 = set(str1.split())
        words2 = set(str2.split())
        
        # Calculate Jaccard similarity
        intersection = len(words1 & words2)
        union = len(words1 | words2)
        
        if union == 0:
            return 0
        
        return (intersection / union) * 100
    
    def merge_duplicates(self, keep_id: int, remove_id: int):
        """
        Merge duplicate jobs (keep one, remove other)
        
        Args:
            keep_id: ID of job to keep
            remove_id: ID of job to remove
        """
        try:
            keep_job = self.db.query(Job).get(keep_id)
            remove_job = self.db.query(Job).get(remove_id)
            
            if not keep_job or not remove_job:
                logger.error(f"Jobs not found: {keep_id}, {remove_id}")
                return
            
            # Merge information (keep more complete data)
            if not keep_job.description and remove_job.description:
                keep_job.description = remove_job.description
            
            if not keep_job.requirements and remove_job.requirements:
                keep_job.requirements = remove_job.requirements
            
            if not keep_job.benefits and remove_job.benefits:
                keep_job.benefits = remove_job.benefits
            
            if not keep_job.salary and remove_job.salary:
                keep_job.salary = remove_job.salary
            
            # Mark removed job as duplicate
            remove_job.is_duplicate = True
            remove_job.duplicate_of = keep_id
            
            self.db.commit()
            logger.info(f"Merged job {remove_id} into {keep_id}")
        
        except Exception as e:
            logger.error(f"Error merging duplicates: {e}")
            self.db.rollback()
