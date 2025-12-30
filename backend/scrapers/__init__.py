"""
Scrapers package for SmartJobHunter Pro
"""
from scrapers.base_scraper import BaseScraper
from scrapers.arbeitsagentur import ArbeitsagenturScraper
from scrapers.jobspy_scraper import JobSpyScraper
from scrapers.aggregators import KimetaScraper, JobliftScraper, JoobleScraper
from scrapers.company_scraper import CompanyScraper
from scrapers.scraper_manager import ScraperManager

__all__ = [
    "BaseScraper",
    "ArbeitsagenturScraper",
    "JobSpyScraper",
    "KimetaScraper",
    "JobliftScraper",
    "JoobleScraper",
    "CompanyScraper",
    "ScraperManager",
]
