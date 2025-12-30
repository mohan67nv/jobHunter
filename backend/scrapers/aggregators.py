"""
Aggregator scrapers - Kimeta, Joblift, Jooble
These sites use JavaScript rendering, so we use Selenium
"""
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from scrapers.base_scraper import BaseScraper
import re

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    from selenium.common.exceptions import TimeoutException, NoSuchElementException
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False
    webdriver = None  # Set to None if not available

try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False


class AggregatorScraper(BaseScraper):
    """Base class for aggregator scrapers using Selenium"""
    
    def __init__(self):
        super().__init__()
        if not SELENIUM_AVAILABLE:
            self.logger.warning("⚠️  Selenium not installed")
        if not BS4_AVAILABLE:
            self.logger.warning("⚠️  BeautifulSoup4 not installed")
    
    def _get_driver(self):
        """Create and configure Selenium WebDriver"""
        if not SELENIUM_AVAILABLE:
            return None
        
        try:
            options = Options()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument(f'user-agent={self.delay_min}')
            
            driver = webdriver.Chrome(options=options)
            driver.set_page_load_timeout(30)
            return driver
        
        except Exception as e:
            self.logger.error(f"Error creating WebDriver: {e}")
            return None
    
    def _parse_relative_date(self, date_str: str) -> datetime:
        """Parse relative dates like 'vor 2 Tagen', 'heute', 'gestern'"""
        date_str = date_str.lower().strip()
        now = datetime.now()
        
        if 'heute' in date_str or 'today' in date_str:
            return now
        elif 'gestern' in date_str or 'yesterday' in date_str:
            return now - timedelta(days=1)
        
        # Parse "vor X Tagen/Stunden"
        match = re.search(r'(\d+)', date_str)
        if match:
            number = int(match.group(1))
            if 'stunde' in date_str or 'hour' in date_str:
                return now - timedelta(hours=number)
            elif 'tag' in date_str or 'day' in date_str:
                return now - timedelta(days=number)
            elif 'woche' in date_str or 'week' in date_str:
                return now - timedelta(weeks=number)
        
        return now


class KimetaScraper(AggregatorScraper):
    """Scraper for Kimeta.de - German job aggregator"""
    
    BASE_URL = "https://www.kimeta.de"
    
    def scrape(self, keyword: str, location: str = "Germany", max_pages: int = 5, **kwargs) -> List[Dict]:
        """
        Scrape jobs from Kimeta
        
        Args:
            keyword: Search keyword
            location: Location
            max_pages: Maximum number of pages to scrape
            
        Returns:
            List of normalized job dictionaries
        """
        if not SELENIUM_AVAILABLE:
            self.logger.error("❌ Selenium not available")
            return []
        
        self.logger.info(f"🔍 Scraping Kimeta for '{keyword}' in '{location}'...")
        
        jobs = []
        driver = self._get_driver()
        
        if not driver:
            return jobs
        
        try:
            for page in range(1, max_pages + 1):
                search_url = f"{self.BASE_URL}/jobs/{keyword.replace(' ', '-')}"
                if page > 1:
                    search_url += f"?page={page}"
                
                self.logger.debug(f"Fetching page {page}: {search_url}")
                driver.get(search_url)
                
                # Wait for job cards to load
                try:
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "job-item"))
                    )
                except TimeoutException:
                    self.logger.warning(f"Timeout waiting for jobs on page {page}")
                    break
                
                # Parse page with BeautifulSoup
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                job_cards = soup.find_all('div', class_='job-item')
                
                if not job_cards:
                    self.logger.info(f"No jobs found on page {page}")
                    break
                
                for card in job_cards:
                    try:
                        job = self._parse_kimeta_job(card)
                        if job and self.validate_job(job):
                            jobs.append(job)
                    except Exception as e:
                        self.logger.error(f"Error parsing Kimeta job: {e}")
                        continue
                
                self.random_delay()
        
        except Exception as e:
            self.logger.error(f"❌ Error scraping Kimeta: {e}")
        
        finally:
            driver.quit()
        
        self.log_scraping_stats(jobs)
        return jobs
    
    def _parse_kimeta_job(self, card) -> Optional[Dict]:
        """Parse Kimeta job card"""
        try:
            title = card.find('h2', class_='job-title')
            title = title.get_text(strip=True) if title else ""
            
            company = card.find('span', class_='company-name')
            company = company.get_text(strip=True) if company else "Unknown"
            
            location = card.find('span', class_='location')
            location = location.get_text(strip=True) if location else "Germany"
            
            link = card.find('a', class_='job-link')
            url = self.BASE_URL + link['href'] if link and 'href' in link.attrs else ""
            
            description = card.find('div', class_='job-description')
            description = description.get_text(strip=True) if description else ""
            
            date_elem = card.find('span', class_='posted-date')
            date_str = date_elem.get_text(strip=True) if date_elem else ""
            posted_date = self._parse_relative_date(date_str)
            
            raw_job = {
                "title": title,
                "company": company,
                "location": location,
                "url": url,
                "description": description,
                "posted_date": posted_date,
            }
            
            return self.normalize_job(raw_job)
        
        except Exception as e:
            self.logger.error(f"Error parsing Kimeta job card: {e}")
            return None


class JobliftScraper(AggregatorScraper):
    """Scraper for Joblift.de - German job aggregator"""
    
    BASE_URL = "https://www.joblift.de"
    
    def scrape(self, keyword: str, location: str = "Germany", max_pages: int = 5, **kwargs) -> List[Dict]:
        """Scrape jobs from Joblift"""
        if not SELENIUM_AVAILABLE:
            self.logger.error("❌ Selenium not available")
            return []
        
        self.logger.info(f"🔍 Scraping Joblift for '{keyword}' in '{location}'...")
        
        jobs = []
        driver = self._get_driver()
        
        if not driver:
            return jobs
        
        try:
            search_url = f"{self.BASE_URL}/stellenangebote/{keyword.replace(' ', '-')}"
            self.logger.debug(f"Fetching: {search_url}")
            driver.get(search_url)
            
            # Wait for job list
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "search-result"))
                )
            except TimeoutException:
                self.logger.warning("Timeout waiting for Joblift results")
                return jobs
            
            # Scroll to load more jobs (infinite scroll)
            for _ in range(max_pages):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                self.random_delay()
            
            # Parse all loaded jobs
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            job_cards = soup.find_all('div', class_='search-result')
            
            for card in job_cards:
                try:
                    job = self._parse_joblift_job(card)
                    if job and self.validate_job(job):
                        jobs.append(job)
                except Exception as e:
                    self.logger.error(f"Error parsing Joblift job: {e}")
                    continue
        
        except Exception as e:
            self.logger.error(f"❌ Error scraping Joblift: {e}")
        
        finally:
            driver.quit()
        
        self.log_scraping_stats(jobs)
        return jobs
    
    def _parse_joblift_job(self, card) -> Optional[Dict]:
        """Parse Joblift job card"""
        try:
            title = card.find('h2')
            title = title.get_text(strip=True) if title else ""
            
            company = card.find('span', class_='company')
            company = company.get_text(strip=True) if company else "Unknown"
            
            location = card.find('span', class_='location')
            location = location.get_text(strip=True) if location else "Germany"
            
            link = card.find('a')
            url = link['href'] if link and 'href' in link.attrs else ""
            if url and not url.startswith('http'):
                url = self.BASE_URL + url
            
            description = card.find('p', class_='description')
            description = description.get_text(strip=True) if description else ""
            
            posted_date = datetime.now()  # Joblift doesn't always show dates
            
            raw_job = {
                "title": title,
                "company": company,
                "location": location,
                "url": url,
                "description": description,
                "posted_date": posted_date,
            }
            
            return self.normalize_job(raw_job)
        
        except Exception as e:
            self.logger.error(f"Error parsing Joblift job card: {e}")
            return None


class JoobleScraper(AggregatorScraper):
    """Scraper for Jooble.org - International job aggregator"""
    
    BASE_URL = "https://de.jooble.org"
    
    def scrape(self, keyword: str, location: str = "Germany", max_pages: int = 5, **kwargs) -> List[Dict]:
        """Scrape jobs from Jooble"""
        if not SELENIUM_AVAILABLE:
            self.logger.error("❌ Selenium not available")
            return []
        
        self.logger.info(f"🔍 Scraping Jooble for '{keyword}' in '{location}'...")
        
        jobs = []
        driver = self._get_driver()
        
        if not driver:
            return jobs
        
        try:
            for page in range(1, max_pages + 1):
                search_url = f"{self.BASE_URL}/stellenangebote-{keyword.replace(' ', '-')}"
                if page > 1:
                    search_url += f"?p={page}"
                
                self.logger.debug(f"Fetching page {page}: {search_url}")
                driver.get(search_url)
                
                # Wait for results
                try:
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "vacancy-item"))
                    )
                except TimeoutException:
                    self.logger.warning(f"Timeout on page {page}")
                    break
                
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                job_cards = soup.find_all('article', class_='vacancy-item')
                
                if not job_cards:
                    break
                
                for card in job_cards:
                    try:
                        job = self._parse_jooble_job(card)
                        if job and self.validate_job(job):
                            jobs.append(job)
                    except Exception as e:
                        self.logger.error(f"Error parsing Jooble job: {e}")
                        continue
                
                self.random_delay()
        
        except Exception as e:
            self.logger.error(f"❌ Error scraping Jooble: {e}")
        
        finally:
            driver.quit()
        
        self.log_scraping_stats(jobs)
        return jobs
    
    def _parse_jooble_job(self, card) -> Optional[Dict]:
        """Parse Jooble job card"""
        try:
            title = card.find('h2')
            title = title.get_text(strip=True) if title else ""
            
            company = card.find('span', class_='company-name')
            company = company.get_text(strip=True) if company else "Unknown"
            
            location = card.find('span', class_='location')
            location = location.get_text(strip=True) if location else "Germany"
            
            link = card.find('a')
            url = link['href'] if link and 'href' in link.attrs else ""
            
            description = card.find('div', class_='description')
            description = description.get_text(strip=True) if description else ""
            
            date_elem = card.find('span', class_='date')
            date_str = date_elem.get_text(strip=True) if date_elem else ""
            posted_date = self._parse_relative_date(date_str)
            
            raw_job = {
                "title": title,
                "company": company,
                "location": location,
                "url": url,
                "description": description,
                "posted_date": posted_date,
            }
            
            return self.normalize_job(raw_job)
        
        except Exception as e:
            self.logger.error(f"Error parsing Jooble job card: {e}")
            return None
