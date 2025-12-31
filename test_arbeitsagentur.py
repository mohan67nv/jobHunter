#!/usr/bin/env python3
"""Test Arbeitsagentur scraper integration"""
import sys
sys.path.insert(0, '/app/backend')

from scrapers.scraper_manager import ScraperManager
from database import SessionLocal
from models.job import Job

print("Testing Arbeitsagentur Integration\n" + "="*80)

db = SessionLocal()
manager = ScraperManager(db)

print("\n1. Starting scrape...")
stats = manager.scrape_all('Python Developer', 'Berlin', sources=['arbeitsagentur'])

print(f"\n2. Scraping Statistics:")
print(f"   Total found: {stats['total_found']}")
print(f"   Total new: {stats['total_new']}")
print(f"   Total updated: {stats['total_updated']}")
print(f"   Duplicates: {stats['duplicates_found']}")

print(f"\n3. Checking database...")
arbeitsagentur_jobs = db.query(Job).filter(Job.source == 'Arbeitsagentur').all()
print(f"   ✅ {len(arbeitsagentur_jobs)} Arbeitsagentur jobs in database")

if arbeitsagentur_jobs:
    print(f"\n4. Sample Jobs:")
    for i, job in enumerate(arbeitsagentur_jobs[:3], 1):
        print(f"\n   {i}. {job.title}")
        print(f"      Company: {job.company}")
        print(f"      Location: {job.location}")
        print(f"      Posted: {job.posted_date}")
        print(f"      URL: {job.url[:70]}...")
        print(f"      Source: {job.source}")

print("\n" + "="*80)
print("Test complete!")

db.close()
