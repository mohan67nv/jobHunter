"""
Automated Scheduler Service
Runs scheduled tasks: daily scraping (2x per day) and match score calculation
"""
import schedule
import time
import logging
from datetime import datetime
from database import SessionLocal
from scrapers.scraper_manager import ScraperManager
from ai_agents.matcher import ResumeMatcher
from models.job import Job, JobAnalysis
from models.user import UserProfile

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def run_daily_scraping():
    """Run automated job scraping with default search terms"""
    logger.info("🚀 Starting scheduled job scraping...")
    
    try:
        db = SessionLocal()
        manager = ScraperManager(db)
        
        # Get user's search keywords from profile
        user = db.query(UserProfile).first()
        if user and user.search_keywords:
            keywords = user.search_keywords.split(',')
        else:
            # Default keywords if no user profile
            keywords = ['Python Developer', 'Software Engineer', 'Data Scientist']
        
        # Scrape for each keyword
        total_new = 0
        for keyword in keywords:
            keyword = keyword.strip()
            logger.info(f"Scraping for: {keyword}")
            
            stats = manager.scrape_all(
                keyword=keyword,
                location=user.preferred_locations if user else 'Germany',
                sources=None  # All sources
            )
            
            total_new += stats['total_new']
            logger.info(f"  Found {stats['total_found']} jobs, {stats['total_new']} new")
        
        logger.info(f"✅ Scraping complete: {total_new} total new jobs added")
        db.close()
        
    except Exception as e:
        logger.error(f"❌ Scraping failed: {e}", exc_info=True)


def calculate_match_scores():
    """Calculate match scores for any jobs that were missed during scraping"""
    logger.info("🧮 Checking for jobs without match scores...")
    
    try:
        db = SessionLocal()
        
        # Get jobs without analysis (edge cases that were missed)
        jobs_to_analyze = db.query(Job).outerjoin(JobAnalysis).filter(
            Job.is_active == True,
            (JobAnalysis.id == None)  # No analysis yet
        ).limit(50).all()  # Process 50 jobs at a time
        
        if not jobs_to_analyze:
            logger.info("No jobs need analysis")
            db.close()
            return
        
        logger.info(f"Analyzing {len(jobs_to_analyze)} jobs...")
        
        # Get user profile for matching
        user = db.query(UserProfile).first()
        if not user:
            logger.warning("No user profile found, skipping match score calculation")
            db.close()
            return
        
        # Initialize matcher
        matcher = ResumeMatcher()
        
        analyzed_count = 0
        for job in jobs_to_analyze:
            try:
                # Calculate match score
                result = matcher.analyze_job_fit(job, user)
                
                # Create or update analysis
                existing_analysis = db.query(JobAnalysis).filter(
                    JobAnalysis.job_id == job.id
                ).first()
                
                if existing_analysis:
                    # Update existing
                    existing_analysis.match_score = result.get('match_score', 0)
                    existing_analysis.matching_skills = ', '.join(result.get('skills_matched', []))
                    existing_analysis.missing_skills = ', '.join(result.get('skills_missing', []))
                else:
                    # Create new
                    analysis = JobAnalysis(
                        job_id=job.id,
                        match_score=result.get('match_score', 0),
                        matching_skills=', '.join(result.get('skills_matched', [])),
                        missing_skills=', '.join(result.get('skills_missing', []))
                    )
                    db.add(analysis)
                
                analyzed_count += 1
                
                if analyzed_count % 10 == 0:
                    db.commit()
                    logger.info(f"  Analyzed {analyzed_count}/{len(jobs_to_analyze)} jobs")
                    
            except Exception as e:
                logger.error(f"Error analyzing job {job.id}: {e}")
                continue
        
        db.commit()
        logger.info(f"✅ Match score calculation complete: {analyzed_count} jobs analyzed")
        db.close()
        
    except Exception as e:
        logger.error(f"❌ Match score calculation failed: {e}", exc_info=True)


def run_scheduler():
    """Main scheduler loop"""
    logger.info("=" * 80)
    logger.info("🕐 Job Hunter Scheduler Service Started")
    logger.info("=" * 80)
    logger.info("Schedule:")
    logger.info("  - Job scraping: 5 times daily (7 AM, 11 AM, 2 PM, 5 PM, 8 PM)")
    logger.info("  - Match score calculation: Every 5 minutes (for any missed jobs)")
    logger.info("  - Note: New jobs get scored immediately during scraping")
    logger.info("=" * 80)
    
    # Schedule daily scraping (5 times per day for maximum job coverage)
    schedule.every().day.at("07:00").do(run_daily_scraping)  # Morning
    schedule.every().day.at("11:00").do(run_daily_scraping)  # Late morning
    schedule.every().day.at("14:00").do(run_daily_scraping)  # Afternoon
    schedule.every().day.at("17:00").do(run_daily_scraping)  # Evening
    schedule.every().day.at("20:00").do(run_daily_scraping)  # Night
    
    # Schedule match score calculation every 5 minutes (for any missed jobs)
    # Note: Most jobs are scored immediately during scraping
    schedule.every(5).minutes.do(calculate_match_scores)
    
    # Run initial match score calculation on startup
    logger.info("Running initial match score calculation...")
    calculate_match_scores()
    
    # Main loop
    while True:
        try:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            logger.info("Scheduler stopped by user")
            break
        except Exception as e:
            logger.error(f"Scheduler error: {e}", exc_info=True)
            time.sleep(60)


if __name__ == "__main__":
    run_scheduler()
