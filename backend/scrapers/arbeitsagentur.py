"""
Arbeitsagentur API scraper - German Federal Employment Agency
Official job board API - no API key required
"""
import requests
from typing import List, Dict, Optional
from datetime import datetime
from scrapers.base_scraper import BaseScraper


class ArbeitsagenturScraper(BaseScraper):
    """Scraper for Arbeitsagentur job board (official German API)"""
    
    BASE_URL = "https://rest.arbeitsagentur.de/jobboerse/jobsuche-service/pc/v4/jobs"
    
    def __init__(self):
        super().__init__()
        self.headers = {
            "User-Agent": "SmartJobHunter/1.0",
            "Accept": "application/json",
        }
    
    def scrape(self, keyword: str, location: str = "Germany", radius: int = 50, 
               max_results: int = 500, **kwargs) -> List[Dict]:
        """
        Scrape jobs from Arbeitsagentur API
        
        Args:
            keyword: Search keyword (e.g., "Data Scientist")
            location: Location to search (city or region)
            radius: Search radius in km
            max_results: Maximum number of jobs to retrieve
            
        Returns:
            List of normalized job dictionaries
        """
        self.logger.info(f"🔍 Scraping Arbeitsagentur for '{keyword}' in '{location}'...")
        
        jobs = []
        page = 0
        page_size = 50  # API limit per page
        
        try:
            while len(jobs) < max_results:
                params = {
                    "was": keyword,
                    "wo": location,
                    "umkreis": radius,
                    "page": page,
                    "size": page_size,
                    "angebotsart": "1",  # 1=employment, 2=self-employment, 4=training
                }
                
                self.logger.debug(f"Fetching page {page + 1}...")
                response = requests.get(self.BASE_URL, params=params, headers=self.headers, timeout=30)
                response.raise_for_status()
                
                data = response.json()
                
                # Check if we have results
                stellenangebote = data.get("stellenangebote", [])
                if not stellenangebote:
                    self.logger.info("No more jobs found")
                    break
                
                # Parse jobs
                for job_data in stellenangebote:
                    try:
                        job = self._parse_job(job_data)
                        if job and self.validate_job(job):
                            jobs.append(job)
                    except Exception as e:
                        self.logger.error(f"Error parsing job: {e}")
                        continue
                
                # Check if we've reached the end
                total_jobs = data.get("maxErgebnisse", 0)
                if len(jobs) >= total_jobs or len(stellenangebote) < page_size:
                    break
                
                page += 1
                self.random_delay()
        
        except requests.RequestException as e:
            self.logger.error(f"❌ Error scraping Arbeitsagentur: {e}")
        
        self.log_scraping_stats(jobs)
        return jobs
    
    def _parse_job(self, job_data: Dict) -> Optional[Dict]:
        """Parse raw Arbeitsagentur job data to normalized format"""
        try:
            # Extract job details
            refnr = job_data.get("refnr", "")
            title = job_data.get("titel", "")
            company = job_data.get("arbeitgeber", "Unknown")
            location = job_data.get("arbeitsort", {}).get("ort", "Germany")
            
            # Job URL - construct from reference number
            url = f"https://www.arbeitsagentur.de/jobsuche/jobdetails/{refnr}"
            
            # Posted date
            posted_date_str = job_data.get("aktuelleVeroeffentlichungsdatum", "")
            try:
                posted_date = datetime.fromisoformat(posted_date_str.replace("Z", "+00:00"))
            except:
                posted_date = datetime.now()
            
            # Description (limited in list view, full details require individual fetch)
            description = job_data.get("beruf", "") + "\n" + job_data.get("taetigkeit", "")
            
            # Employment type
            angebotsart = job_data.get("angebotsart", "")
            job_type = self._map_employment_type(angebotsart)
            
            # Entry date
            eintrittsdatum = job_data.get("eintrittsdatum", "")
            
            raw_job = {
                "title": title,
                "company": company,
                "location": location,
                "url": url,
                "description": description,
                "posted_date": posted_date,
                "job_type": job_type,
                "contract_type": None,
                "remote_type": None,
                "experience_level": None,
                "salary": None,
                "requirements": None,
                "benefits": None,
            }
            
            return self.normalize_job(raw_job)
        
        except Exception as e:
            self.logger.error(f"Error parsing Arbeitsagentur job: {e}")
            return None
    
    def _map_employment_type(self, angebotsart: str) -> Optional[str]:
        """Map Arbeitsagentur employment type codes"""
        mapping = {
            "1": "full-time",
            "2": "part-time",
            "4": "internship",
        }
        return mapping.get(angebotsart)
    
    def get_job_details(self, refnr: str) -> Optional[Dict]:
        """
        Fetch full job details by reference number
        
        Args:
            refnr: Job reference number
            
        Returns:
            Detailed job dictionary
        """
        try:
            url = f"https://rest.arbeitsagentur.de/jobboerse/jobsuche-service/pc/v2/jobdetails/{refnr}"
            response = requests.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            # Parse detailed information
            job_data = {
                "title": data.get("titel", ""),
                "company": data.get("arbeitgeber", ""),
                "description": data.get("stellenbeschreibung", ""),
                "requirements": data.get("anforderungen", ""),
                "benefits": data.get("arbeitgeberdarstellung", ""),
                # Add more fields as needed
            }
            
            return job_data
        
        except Exception as e:
            self.logger.error(f"Error fetching job details for {refnr}: {e}")
            return None
