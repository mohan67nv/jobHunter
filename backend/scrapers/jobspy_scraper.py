"""
JobSpy integration scraper - supports LinkedIn, Indeed, StepStone, Glassdoor
Uses python-jobspy library for multi-portal scraping
"""
from typing import List, Dict, Optional
from datetime import datetime
from scrapers.base_scraper import BaseScraper

try:
    from jobspy import scrape_jobs
    JOBSPY_AVAILABLE = True
except ImportError:
    JOBSPY_AVAILABLE = False


class JobSpyScraper(BaseScraper):
    """Scraper using JobSpy library for multiple job portals"""
    
    SUPPORTED_SITES = ["linkedin", "indeed", "stepstone", "glassdoor"]
    
    def __init__(self):
        super().__init__()
        if not JOBSPY_AVAILABLE:
            self.logger.warning("⚠️  python-jobspy not installed. Install with: pip install python-jobspy")
    
    def scrape(self, keyword: str, location: str = "Germany", sites: List[str] = None,
               results_wanted: int = 100, **kwargs) -> List[Dict]:
        """
        Scrape jobs using JobSpy from multiple sites
        
        Args:
            keyword: Search keyword
            location: Location to search
            sites: List of sites to scrape (default: all supported)
            results_wanted: Number of results per site
            
        Returns:
            List of normalized job dictionaries
        """
        if not JOBSPY_AVAILABLE:
            self.logger.error("❌ JobSpy not available")
            return []
        
        if sites is None:
            sites = self.SUPPORTED_SITES
        
        self.logger.info(f"🔍 Scraping {', '.join(sites)} for '{keyword}' in '{location}'...")
        
        all_jobs = []
        
        for site in sites:
            try:
                self.logger.info(f"  Scraping {site}...")
                
                # JobSpy scrape_jobs function
                jobs_df = scrape_jobs(
                    site_name=site,
                    search_term=keyword,
                    location=location,
                    results_wanted=results_wanted,
                    country_indeed="Germany" if site == "indeed" else "usa",
                    full_description=True,  # Get full job descriptions
                )
                
                if jobs_df is not None and not jobs_df.empty:
                    # Convert DataFrame to list of dicts
                    for _, row in jobs_df.iterrows():
                        try:
                            job = self._parse_jobspy_row(row, site)
                            if job and self.validate_job(job):
                                all_jobs.append(job)
                        except Exception as e:
                            self.logger.error(f"Error parsing {site} job: {e}")
                            continue
                    
                    self.logger.info(f"  ✅ {site}: {len(jobs_df)} jobs scraped")
                else:
                    self.logger.warning(f"  ⚠️  {site}: No jobs found")
                
                self.random_delay()
            
            except Exception as e:
                self.logger.error(f"  ❌ {site}: Error - {e}")
                continue
        
        self.log_scraping_stats(all_jobs)
        return all_jobs
    
    def _parse_jobspy_row(self, row, site: str) -> Optional[Dict]:
        """Parse JobSpy DataFrame row to normalized format"""
        try:
            # JobSpy standard columns
            title = str(row.get("title", ""))
            company = str(row.get("company", ""))
            location = str(row.get("location", ""))
            description = str(row.get("description", ""))
            url = str(row.get("job_url", ""))
            
            # Date posted
            date_posted = row.get("date_posted")
            if isinstance(date_posted, str):
                try:
                    posted_date = datetime.fromisoformat(date_posted)
                except:
                    posted_date = datetime.now()
            else:
                posted_date = datetime.now()
            
            # Salary
            salary_min = row.get("min_amount")
            salary_max = row.get("max_amount")
            salary = None
            if salary_min and salary_max:
                salary = f"€{salary_min:,.0f} - €{salary_max:,.0f}"
            elif salary_min:
                salary = f"€{salary_min:,.0f}+"
            
            # Job type
            job_type = row.get("job_type")
            if job_type:
                job_type = str(job_type).lower()
            
            raw_job = {
                "title": title,
                "company": company,
                "location": location,
                "url": url,
                "description": description,
                "posted_date": posted_date,
                "salary": salary,
                "job_type": job_type,
                "contract_type": None,
                "remote_type": None,
                "experience_level": None,
                "requirements": None,
                "benefits": None,
            }
            
            # Set source to specific site
            normalized = self.normalize_job(raw_job)
            normalized["source"] = site.title()
            
            return normalized
        
        except Exception as e:
            self.logger.error(f"Error parsing JobSpy row: {e}")
            return None
    
    def scrape_linkedin(self, keyword: str, location: str = "Germany", **kwargs) -> List[Dict]:
        """Convenience method to scrape LinkedIn only"""
        return self.scrape(keyword, location, sites=["linkedin"], **kwargs)
    
    def scrape_indeed(self, keyword: str, location: str = "Germany", **kwargs) -> List[Dict]:
        """Convenience method to scrape Indeed only"""
        return self.scrape(keyword, location, sites=["indeed"], **kwargs)
    
    def scrape_stepstone(self, keyword: str, location: str = "Germany", **kwargs) -> List[Dict]:
        """Convenience method to scrape StepStone only"""
        return self.scrape(keyword, location, sites=["stepstone"], **kwargs)
    
    def scrape_glassdoor(self, keyword: str, location: str = "Germany", **kwargs) -> List[Dict]:
        """Convenience method to scrape Glassdoor only"""
        return self.scrape(keyword, location, sites=["glassdoor"], **kwargs)
