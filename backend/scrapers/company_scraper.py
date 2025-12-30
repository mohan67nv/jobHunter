"""
Company career page scraper
Scrapes jobs directly from company career pages
Supports common ATS platforms: Greenhouse, Workday, Lever, custom HTML
"""
from typing import List, Dict, Optional
from datetime import datetime
from scrapers.base_scraper import BaseScraper
import requests

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False

try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False


class CompanyScraper(BaseScraper):
    """Scraper for company career pages"""
    
    def __init__(self):
        super().__init__()
        self.ats_detectors = {
            'greenhouse': self._scrape_greenhouse,
            'workday': self._scrape_workday,
            'lever': self._scrape_lever,
            'smartrecruiters': self._scrape_smartrecruiters,
        }
    
    def scrape(self, company_name: str, career_url: str, **kwargs) -> List[Dict]:
        """
        Scrape jobs from company career page
        
        Args:
            company_name: Name of company
            career_url: URL of career page
            
        Returns:
            List of normalized job dictionaries
        """
        self.logger.info(f"🔍 Scraping {company_name} career page...")
        
        # Detect ATS platform
        ats_type = self._detect_ats(career_url)
        self.logger.debug(f"Detected ATS: {ats_type or 'custom'}")
        
        # Use appropriate scraper
        if ats_type and ats_type in self.ats_detectors:
            jobs = self.ats_detectors[ats_type](company_name, career_url)
        else:
            jobs = self._scrape_custom(company_name, career_url)
        
        # Set company name for all jobs
        for job in jobs:
            job['company'] = company_name
        
        self.log_scraping_stats(jobs)
        return jobs
    
    def _detect_ats(self, url: str) -> Optional[str]:
        """Detect ATS platform from URL patterns"""
        url_lower = url.lower()
        
        if 'greenhouse.io' in url_lower or 'boards.greenhouse.io' in url_lower:
            return 'greenhouse'
        elif 'myworkdayjobs.com' in url_lower or 'workday' in url_lower:
            return 'workday'
        elif 'lever.co' in url_lower or 'jobs.lever.co' in url_lower:
            return 'lever'
        elif 'smartrecruiters.com' in url_lower:
            return 'smartrecruiters'
        
        return None
    
    def _scrape_greenhouse(self, company_name: str, url: str) -> List[Dict]:
        """Scrape Greenhouse ATS"""
        jobs = []
        
        try:
            # Greenhouse has a JSON API
            if 'boards.greenhouse.io' in url:
                # Extract board token
                board_token = url.split('/')[-1]
                api_url = f"https://boards-api.greenhouse.io/v1/boards/{board_token}/jobs"
            else:
                api_url = url
            
            response = requests.get(api_url, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            job_list = data.get('jobs', [])
            
            for job_data in job_list:
                try:
                    job = {
                        "title": job_data.get('title', ''),
                        "company": company_name,
                        "location": job_data.get('location', {}).get('name', ''),
                        "url": job_data.get('absolute_url', ''),
                        "description": job_data.get('content', ''),
                        "posted_date": datetime.now(),
                    }
                    
                    normalized = self.normalize_job(job)
                    if self.validate_job(normalized):
                        jobs.append(normalized)
                
                except Exception as e:
                    self.logger.error(f"Error parsing Greenhouse job: {e}")
                    continue
        
        except Exception as e:
            self.logger.error(f"Error scraping Greenhouse: {e}")
        
        return jobs
    
    def _scrape_workday(self, company_name: str, url: str) -> List[Dict]:
        """Scrape Workday ATS (requires Selenium)"""
        if not SELENIUM_AVAILABLE:
            self.logger.error("Selenium required for Workday")
            return []
        
        jobs = []
        driver = self._get_driver()
        
        if not driver:
            return jobs
        
        try:
            driver.get(url)
            
            # Wait for job listings
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-automation-id='jobTitle']"))
            )
            
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            job_elements = soup.find_all('li', {'class': 'css-1q2dra3'})  # Common Workday class
            
            for elem in job_elements:
                try:
                    title_elem = elem.find('a', {'data-automation-id': 'jobTitle'})
                    title = title_elem.get_text(strip=True) if title_elem else ""
                    job_url = title_elem['href'] if title_elem and 'href' in title_elem.attrs else ""
                    
                    if job_url and not job_url.startswith('http'):
                        job_url = url.split('/careers')[0] + job_url
                    
                    location_elem = elem.find('dd', {'data-automation-id': 'location'})
                    location = location_elem.get_text(strip=True) if location_elem else ""
                    
                    job = {
                        "title": title,
                        "company": company_name,
                        "location": location,
                        "url": job_url,
                        "description": "",  # Would need to fetch individual page
                        "posted_date": datetime.now(),
                    }
                    
                    normalized = self.normalize_job(job)
                    if self.validate_job(normalized):
                        jobs.append(normalized)
                
                except Exception as e:
                    self.logger.error(f"Error parsing Workday job: {e}")
                    continue
        
        except Exception as e:
            self.logger.error(f"Error scraping Workday: {e}")
        
        finally:
            driver.quit()
        
        return jobs
    
    def _scrape_lever(self, company_name: str, url: str) -> List[Dict]:
        """Scrape Lever ATS"""
        jobs = []
        
        try:
            # Lever has a JSON API
            if 'jobs.lever.co' in url:
                company_slug = url.split('/')[-1]
                api_url = f"https://api.lever.co/v0/postings/{company_slug}"
            else:
                return []
            
            response = requests.get(api_url, timeout=30)
            response.raise_for_status()
            
            job_list = response.json()
            
            for job_data in job_list:
                try:
                    job = {
                        "title": job_data.get('text', ''),
                        "company": company_name,
                        "location": job_data.get('categories', {}).get('location', ''),
                        "url": job_data.get('hostedUrl', ''),
                        "description": job_data.get('description', ''),
                        "posted_date": datetime.fromtimestamp(job_data.get('createdAt', 0) / 1000),
                    }
                    
                    normalized = self.normalize_job(job)
                    if self.validate_job(normalized):
                        jobs.append(normalized)
                
                except Exception as e:
                    self.logger.error(f"Error parsing Lever job: {e}")
                    continue
        
        except Exception as e:
            self.logger.error(f"Error scraping Lever: {e}")
        
        return jobs
    
    def _scrape_smartrecruiters(self, company_name: str, url: str) -> List[Dict]:
        """Scrape SmartRecruiters ATS"""
        jobs = []
        
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            job_elements = soup.find_all('li', {'class': 'opening-job'})
            
            for elem in job_elements:
                try:
                    title_elem = elem.find('a')
                    title = title_elem.get_text(strip=True) if title_elem else ""
                    job_url = title_elem['href'] if title_elem and 'href' in title_elem.attrs else ""
                    
                    location_elem = elem.find('span', {'class': 'job-location'})
                    location = location_elem.get_text(strip=True) if location_elem else ""
                    
                    job = {
                        "title": title,
                        "company": company_name,
                        "location": location,
                        "url": job_url,
                        "description": "",
                        "posted_date": datetime.now(),
                    }
                    
                    normalized = self.normalize_job(job)
                    if self.validate_job(normalized):
                        jobs.append(normalized)
                
                except Exception as e:
                    self.logger.error(f"Error parsing SmartRecruiters job: {e}")
                    continue
        
        except Exception as e:
            self.logger.error(f"Error scraping SmartRecruiters: {e}")
        
        return jobs
    
    def _scrape_custom(self, company_name: str, url: str) -> List[Dict]:
        """Fallback scraper for custom career pages"""
        self.logger.info(f"Using custom scraper for {company_name}")
        jobs = []
        
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Try common patterns
            job_elements = (
                soup.find_all('div', {'class': lambda x: x and 'job' in x.lower()}) or
                soup.find_all('li', {'class': lambda x: x and 'job' in x.lower()}) or
                soup.find_all('article', {'class': lambda x: x and 'job' in x.lower()})
            )
            
            for elem in job_elements[:20]:  # Limit to 20 to avoid false positives
                try:
                    # Try to find title
                    title_elem = elem.find(['h2', 'h3', 'h4', 'a'])
                    title = title_elem.get_text(strip=True) if title_elem else ""
                    
                    # Try to find link
                    link_elem = elem.find('a')
                    job_url = link_elem['href'] if link_elem and 'href' in link_elem.attrs else ""
                    
                    if job_url and not job_url.startswith('http'):
                        from urllib.parse import urljoin
                        job_url = urljoin(url, job_url)
                    
                    if title and job_url:
                        job = {
                            "title": title,
                            "company": company_name,
                            "location": "Germany",  # Default
                            "url": job_url,
                            "description": "",
                            "posted_date": datetime.now(),
                        }
                        
                        normalized = self.normalize_job(job)
                        if self.validate_job(normalized):
                            jobs.append(normalized)
                
                except Exception as e:
                    continue
        
        except Exception as e:
            self.logger.error(f"Error scraping custom page: {e}")
        
        return jobs
    
    def _get_driver(self):
        """Create Selenium WebDriver"""
        try:
            options = Options()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            driver = webdriver.Chrome(options=options)
            return driver
        except Exception as e:
            self.logger.error(f"Error creating driver: {e}")
            return None
