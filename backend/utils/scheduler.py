"""
Job scheduler for automated scraping and analysis
Uses APScheduler for background task scheduling
"""
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime
from sqlalchemy.orm import Session
from config import settings
from utils.logger import setup_logger

logger = setup_logger(__name__)


class JobScheduler:
    """Manages scheduled tasks for scraping and analysis"""
    
    def __init__(self, db_factory):
        """
        Initialize scheduler
        
        Args:
            db_factory: Function that returns database session
        """
        self.scheduler = BackgroundScheduler()
        self.db_factory = db_factory
        self.is_running = False
    
    def start(self):
        """Start the scheduler"""
        if self.is_running:
            logger.warning("Scheduler already running")
            return
        
        logger.info("🕐 Starting job scheduler...")
        
        # Schedule scraping tasks
        if settings.scrape_interval_hours > 0:
            self.scheduler.add_job(
                func=self._scheduled_scrape,
                trigger=IntervalTrigger(hours=settings.scrape_interval_hours),
                id='scrape_jobs',
                name='Scrape jobs from all sources',
                replace_existing=True
            )
            logger.info(f"   Scraping scheduled every {settings.scrape_interval_hours} hours")
        
        # Schedule analysis tasks
        if settings.analysis_interval_hours > 0:
            self.scheduler.add_job(
                func=self._scheduled_analysis,
                trigger=IntervalTrigger(hours=settings.analysis_interval_hours),
                id='analyze_jobs',
                name='Analyze new jobs',
                replace_existing=True
            )
            logger.info(f"   Analysis scheduled every {settings.analysis_interval_hours} hours")
        
        self.scheduler.start()
        self.is_running = True
        logger.info("✅ Scheduler started successfully")
    
    def stop(self):
        """Stop the scheduler"""
        if not self.is_running:
            return
        
        logger.info("Stopping scheduler...")
        self.scheduler.shutdown()
        self.is_running = False
        logger.info("✅ Scheduler stopped")
    
    def _scheduled_scrape(self):
        """Scheduled scraping task"""
        logger.info("⏰ Running scheduled scraping...")
        
        try:
            db = self.db_factory()
            
            from scrapers.scraper_manager import ScraperManager
            from models.user import UserProfile
            
            # Get user preferences
            user = db.query(UserProfile).filter(UserProfile.id == 1).first()
            
            if user and user.preferences:
                import json
                prefs = json.loads(user.preferences)
                keywords = prefs.get('keywords', ['Data Scientist'])
                locations = prefs.get('locations', ['Germany'])
            else:
                keywords = ['Data Scientist']
                locations = ['Germany']
            
            # Run scraping
            manager = ScraperManager(db)
            
            for keyword in keywords:
                for location in locations:
                    logger.info(f"Scraping: {keyword} in {location}")
                    stats = manager.scrape_all(keyword, location)
                    logger.info(f"Found {stats['total_new']} new jobs")
            
            db.close()
            logger.info("✅ Scheduled scraping completed")
        
        except Exception as e:
            logger.error(f"❌ Error in scheduled scraping: {e}")
    
    def _scheduled_analysis(self):
        """Scheduled analysis task"""
        logger.info("⏰ Running scheduled analysis...")
        
        try:
            db = self.db_factory()
            
            from models.job import Job, JobAnalysis
            from ai_agents.agent_manager import AgentManager
            
            # Get jobs without analysis
            jobs = db.query(Job)\
                .outerjoin(JobAnalysis)\
                .filter(Job.is_active == True)\
                .filter(JobAnalysis.id == None)\
                .limit(50)\
                .all()
            
            if not jobs:
                logger.info("No jobs to analyze")
                db.close()
                return
            
            logger.info(f"Analyzing {len(jobs)} jobs...")
            
            agent_manager = AgentManager(db)
            
            for job in jobs:
                try:
                    agent_manager.analyze_job(job.id)
                except Exception as e:
                    logger.error(f"Error analyzing job {job.id}: {e}")
                    continue
            
            db.close()
            logger.info("✅ Scheduled analysis completed")
        
        except Exception as e:
            logger.error(f"❌ Error in scheduled analysis: {e}")
    
    def add_job(self, func, trigger, job_id: str, **kwargs):
        """
        Add a custom job to scheduler
        
        Args:
            func: Function to execute
            trigger: APScheduler trigger
            job_id: Unique job identifier
            **kwargs: Additional job parameters
        """
        self.scheduler.add_job(
            func=func,
            trigger=trigger,
            id=job_id,
            replace_existing=True,
            **kwargs
        )
        logger.info(f"Added job: {job_id}")
    
    def remove_job(self, job_id: str):
        """Remove a job from scheduler"""
        try:
            self.scheduler.remove_job(job_id)
            logger.info(f"Removed job: {job_id}")
        except Exception as e:
            logger.error(f"Error removing job {job_id}: {e}")
    
    def get_jobs(self):
        """Get all scheduled jobs"""
        return self.scheduler.get_jobs()


def setup_scheduler(db_factory):
    """
    Setup and start scheduler
    
    Args:
        db_factory: Function that returns database session
        
    Returns:
        JobScheduler instance
    """
    scheduler = JobScheduler(db_factory)
    scheduler.start()
    return scheduler
