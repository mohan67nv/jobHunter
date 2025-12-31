"""
Scraper Manager - orchestrates all scrapers and handles concurrent scraping
"""
from typing import List, Dict, Optional
import asyncio
from datetime import datetime
from sqlalchemy.orm import Session
from models.job import Job
from models.scraping_log import ScrapingLog
from models.company import Company
from models.user import UserProfile
from scrapers.arbeitsagentur import ArbeitsagenturScraper
from scrapers.jobspy_scraper import JobSpyScraper
from scrapers.aggregators import KimetaScraper, JobliftScraper, JoobleScraper
from scrapers.company_scraper import CompanyScraper
from scrapers.german_job_boards import StepStoneScraper, XINGJobsScraper, MonsterDeScraper, FinestJobsScraper
from utils.deduplicator import Deduplicator
from utils.logger import setup_logger

logger = setup_logger(__name__)


class ScraperManager:
    """Manages and orchestrates all job scrapers"""
    
    def __init__(self, db: Session):
        """
        Initialize scraper manager
        
        Args:
            db: Database session
        """
        self.db = db
        self.deduplicator = Deduplicator(db)
        
        # Initialize all scrapers (German boards + aggregators)
        self.scrapers = {
            'arbeitsagentur': ArbeitsagenturScraper(),
            'jobspy': JobSpyScraper(),  # Indeed, LinkedIn, Glassdoor, ZipRecruiter
            'kimeta': KimetaScraper(),  # Meta-aggregator (2000+ sources)
            'joblift': JobliftScraper(),  # Meta-aggregator (4000+ sources)
            'jooble': JoobleScraper(),  # Aggregator
            'stepstone': StepStoneScraper(),  # Premium German board
            'xing': XINGJobsScraper(),  # German professional network
            'monster': MonsterDeScraper(),  # Traditional board
            'finest': FinestJobsScraper(),  # Direct company postings
            'company': CompanyScraper(),
        }
    
    def scrape_all(self, keyword: str, location: str = "Germany", 
                   sources: Optional[List[str]] = None) -> Dict:
        """
        Scrape jobs from all sources
        
        Args:
            keyword: Search keyword
            location: Search location
            sources: List of sources to scrape (None = all)
            
        Returns:
            Dictionary with scraping statistics
        """
        logger.info(f"🚀 Starting scraping for '{keyword}' in '{location}'")
        
        # Default to major German boards + aggregators for comprehensive coverage
        if sources is None or sources == ['all']:
            sources = [
                'jobspy',  # LinkedIn, Indeed, Glassdoor (100+ jobs)
                'kimeta',  # Meta-aggregator (covers 2000+ sources)
                'joblift',  # Meta-aggregator (covers 4000+ sources)
                'arbeitsagentur',  # German federal agency
                'stepstone',  # Premium German board
                'xing',  # German professional network
                'monster',  # Traditional board
                'finest',  # Direct company postings
            ]
        
        all_jobs = []
        stats = {
            'total_found': 0,
            'total_new': 0,
            'total_updated': 0,
            'sources': {}
        }
        
        # Scrape from each source
        for source in sources:
            if source not in self.scrapers:
                logger.warning(f"Unknown source: {source}")
                continue
            
            try:
                scraper = self.scrapers[source]
                started_at = datetime.now()
                
                logger.info(f"📡 Scraping {source}...")
                
                # Handle JobSpy separately (multiple sites)
                if source == 'jobspy':
                    jobs = scraper.scrape(keyword, location, 
                                         sites=['linkedin', 'indeed', 'stepstone', 'glassdoor'],
                                         results_wanted=100)
                else:
                    jobs = scraper.scrape(keyword, location)
                
                completed_at = datetime.now()
                duration = (completed_at - started_at).total_seconds()
                
                # Save jobs to database with deduplication
                new_count, updated_count = self._save_jobs(jobs)
                
                # Cleanup old jobs if we exceed max limit
                self._cleanup_old_jobs()
                
                # Log scraping session
                self._log_scraping(source, len(jobs), new_count, updated_count, 
                                  'success', None, duration, started_at, completed_at)
                
                stats['total_found'] += len(jobs)
                stats['total_new'] += new_count
                stats['total_updated'] += updated_count
                stats['sources'][source] = {
                    'found': len(jobs),
                    'new': new_count,
                    'updated': updated_count,
                    'duration': duration
                }
                
                all_jobs.extend(jobs)
                
            except Exception as e:
                logger.error(f"❌ Error scraping {source}: {e}")
                self._log_scraping(source, 0, 0, 0, 'failed', str(e), 
                                  0, datetime.now(), datetime.now())
                stats['sources'][source] = {'error': str(e)}
        
        # Run deduplication
        logger.info("🔍 Running deduplication...")
        duplicates = self.deduplicator.deduplicate_all()
        stats['duplicates_found'] = len(duplicates)
        
        logger.info(f"✅ Scraping complete: {stats['total_new']} new jobs, "
                   f"{stats['total_updated']} updated, {stats['duplicates_found']} duplicates")
        
        return stats
    
    def scrape_companies(self, keywords: List[str] = None) -> Dict:
        """
        Scrape jobs from company career pages
        
        Args:
            keywords: Optional list of keywords to filter companies
            
        Returns:
            Dictionary with scraping statistics
        """
        logger.info("🏢 Starting company career page scraping...")
        
        # Get active companies from database
        companies = self.db.query(Company).filter(Company.is_active == True).all()
        
        if not companies:
            logger.warning("No companies found in database")
            return {'total_companies': 0, 'total_jobs': 0}
        
        logger.info(f"Found {len(companies)} companies to scrape")
        
        stats = {
            'total_companies': len(companies),
            'total_jobs': 0,
            'total_new': 0,
            'companies': {}
        }
        
        company_scraper = self.scrapers['company']
        
        for company in companies:
            try:
                started_at = datetime.now()
                logger.info(f"📡 Scraping {company.name}...")
                
                jobs = company_scraper.scrape(company.name, company.career_url)
                
                completed_at = datetime.now()
                duration = (completed_at - started_at).total_seconds()
                
                # Save jobs
                new_count, updated_count = self._save_jobs(jobs)
                
                # Update company last_scraped
                company.last_scraped = completed_at
                self.db.commit()
                
                # Log scraping
                self._log_scraping(f"Company: {company.name}", len(jobs), 
                                  new_count, updated_count, 'success', None,
                                  duration, started_at, completed_at)
                
                stats['total_jobs'] += len(jobs)
                stats['total_new'] += new_count
                stats['companies'][company.name] = {
                    'found': len(jobs),
                    'new': new_count,
                    'updated': updated_count
                }
                
            except Exception as e:
                logger.error(f"❌ Error scraping {company.name}: {e}")
                self._log_scraping(f"Company: {company.name}", 0, 0, 0, 
                                  'failed', str(e), 0, datetime.now(), datetime.now())
                stats['companies'][company.name] = {'error': str(e)}
        
        logger.info(f"✅ Company scraping complete: {stats['total_new']} new jobs from {len(companies)} companies")
        
        return stats
    
    def _save_jobs(self, jobs: List[Dict]) -> tuple:
        """
        Save jobs to database with filtering
        
        Args:
            jobs: List of job dictionaries
            
        Returns:
            Tuple of (new_count, updated_count)
        """
        new_count = 0
        updated_count = 0
        
        for job_data in jobs:
            try:
                # FILTER 1: Skip internships
                title = job_data.get('title', '').lower()
                job_type = job_data.get('job_type', '').lower()
                if 'intern' in title or 'praktikum' in title or 'internship' in job_type:
                    logger.debug(f"Skipping internship: {job_data.get('title')}")
                    continue
                
                # FILTER 2: Skip jobs requiring fluent German
                description = (job_data.get('description', '') or '').lower()
                requirements = (job_data.get('requirements', '') or '').lower()
                combined_text = f"{description} {requirements}"
                
                german_required_patterns = [
                    'fluent german', 'fließend deutsch', 'fliessend deutsch',
                    'german fluency', 'deutsch fließend', 'deutsch fliessend',
                    'native german', 'muttersprachler deutsch',
                    'verhandlungssicher deutsch', 'verhandlungssichere deutschkenntnisse',
                    'c1 deutsch', 'c2 deutsch'
                ]
                
                if any(pattern in combined_text for pattern in german_required_patterns):
                    logger.debug(f"Skipping job requiring fluent German: {job_data.get('title')}")
                    continue
                
                # FILTER 3: Only full-time jobs
                if job_type and job_type not in ['full-time', 'full time', 'fulltime', 'vollzeit', '']:
                    logger.debug(f"Skipping non-fulltime job: {job_data.get('title')}")
                    continue
                
                # Check if job already exists by URL
                existing = self.db.query(Job).filter(Job.url == job_data['url']).first()
                
                if existing:
                    # Update existing job
                    for key, value in job_data.items():
                        if hasattr(existing, key) and key not in ['id', 'created_at', 'scraped_date']:
                            setattr(existing, key, value)
                    existing.updated_at = datetime.now()
                    existing.scraped_date = datetime.now()
                    updated_count += 1
                else:
                    # Create new job
                    job = Job(**job_data)
                    self.db.add(job)
                    new_count += 1
                
            except Exception as e:
                logger.error(f"Error saving job: {e}")
                continue
        
        try:
            self.db.commit()
        except Exception as e:
            logger.error(f"Error committing jobs: {e}")
            self.db.rollback()
        
        return new_count, updated_count
    
    def _cleanup_old_jobs(self):
        """Clean up old jobs if database exceeds max limit"""
        from config import settings
        
        try:
            # Count total active jobs
            total_jobs = self.db.query(Job).filter(Job.is_active == True).count()
            max_jobs = getattr(settings, 'max_total_jobs', 5000)
            
            if total_jobs > max_jobs:
                # Calculate how many to delete
                to_delete = total_jobs - max_jobs
                
                logger.info(f"🗑️  Database has {total_jobs} jobs (max: {max_jobs}). Deleting {to_delete} oldest jobs...")
                
                # Get oldest jobs (by posted_date)
                old_jobs = self.db.query(Job)\
                    .filter(Job.is_active == True)\
                    .order_by(Job.posted_date.asc())\
                    .limit(to_delete)\
                    .all()
                
                for job in old_jobs:
                    job.is_active = False  # Soft delete
                
                self.db.commit()
                logger.info(f"✅ Deactivated {to_delete} old jobs")
        except Exception as e:
            logger.error(f"Error cleaning up old jobs: {e}")
            self.db.rollback()
    
    def _log_scraping(self, source: str, jobs_found: int, jobs_new: int, 
                     jobs_updated: int, status: str, error_message: Optional[str],
                     duration: float, started_at: datetime, completed_at: datetime):
        """Log scraping session to database"""
        try:
            log = ScrapingLog(
                source=source,
                jobs_found=jobs_found,
                jobs_new=jobs_new,
                jobs_updated=jobs_updated,
                status=status,
                error_message=error_message,
                duration_seconds=duration,
                started_at=started_at,
                completed_at=completed_at
            )
            self.db.add(log)
            self.db.commit()
        except Exception as e:
            logger.error(f"Error logging scraping session: {e}")
            self.db.rollback()
    
    def get_scraping_history(self, limit: int = 50) -> List[Dict]:
        """
        Get recent scraping history
        
        Args:
            limit: Maximum number of records to return
            
        Returns:
            List of scraping log dictionaries
        """
        logs = self.db.query(ScrapingLog)\
            .order_by(ScrapingLog.started_at.desc())\
            .limit(limit)\
            .all()
        
        return [log.to_dict() for log in logs]
