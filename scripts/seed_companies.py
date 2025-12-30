"""
Seed companies database with German companies
Run this script to populate the companies table
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import SessionLocal, init_db
from models.company import Company
import json

# Sample German companies - expand this list to 500+
GERMAN_COMPANIES = [
    {
        "name": "SAP",
        "career_url": "https://jobs.sap.com/search/",
        "industry": "Enterprise Software",
        "size": "100000+",
        "location": "Walldorf, Germany",
        "description": "Enterprise application software",
        "scrape_frequency": "daily"
    },
    {
        "name": "BMW Group",
        "career_url": "https://www.bmwgroup.jobs/de/en/jobfinder.html",
        "industry": "Automotive",
        "size": "100000+",
        "location": "Munich, Germany",
        "description": "Premium automobile manufacturer",
        "scrape_frequency": "daily"
    },
    {
        "name": "Siemens",
        "career_url": "https://jobs.siemens.com/careers",
        "industry": "Industrial Technology",
        "size": "100000+",
        "location": "Munich, Germany",
        "description": "Industrial manufacturing and technology",
        "scrape_frequency": "daily"
    },
    {
        "name": "Deutsche Bank",
        "career_url": "https://careers.db.com/",
        "industry": "Banking & Finance",
        "size": "50000-100000",
        "location": "Frankfurt, Germany",
        "description": "International banking and financial services",
        "scrape_frequency": "weekly"
    },
    {
        "name": "Allianz",
        "career_url": "https://careers.allianz.com/",
        "industry": "Insurance",
        "size": "100000+",
        "location": "Munich, Germany",
        "description": "Insurance and asset management",
        "scrape_frequency": "weekly"
    },
    {
        "name": "Volkswagen",
        "career_url": "https://www.volkswagen-careers.de/",
        "industry": "Automotive",
        "size": "100000+",
        "location": "Wolfsburg, Germany",
        "description": "Automotive manufacturer",
        "scrape_frequency": "daily"
    },
    {
        "name": "Mercedes-Benz",
        "career_url": "https://www.mercedes-benz.com/en/career/",
        "industry": "Automotive",
        "size": "100000+",
        "location": "Stuttgart, Germany",
        "description": "Luxury automobile manufacturer",
        "scrape_frequency": "daily"
    },
    {
        "name": "Bosch",
        "career_url": "https://www.bosch.com/careers/",
        "industry": "Engineering & Technology",
        "size": "100000+",
        "location": "Stuttgart, Germany",
        "description": "Engineering and technology company",
        "scrape_frequency": "daily"
    },
    {
        "name": "Adidas",
        "career_url": "https://careers.adidas-group.com/",
        "industry": "Sportswear",
        "size": "50000-100000",
        "location": "Herzogenaurach, Germany",
        "description": "Sportswear and equipment",
        "scrape_frequency": "weekly"
    },
    {
        "name": "BASF",
        "career_url": "https://www.basf.com/global/en/careers.html",
        "industry": "Chemicals",
        "size": "100000+",
        "location": "Ludwigshafen, Germany",
        "description": "Chemical company",
        "scrape_frequency": "weekly"
    },
    {
        "name": "Zalando",
        "career_url": "https://jobs.zalando.com/",
        "industry": "E-commerce",
        "size": "10000-50000",
        "location": "Berlin, Germany",
        "description": "Online fashion retailer",
        "scrape_frequency": "daily"
    },
    {
        "name": "Delivery Hero",
        "career_url": "https://careers.deliveryhero.com/",
        "industry": "Food Delivery",
        "size": "10000-50000",
        "location": "Berlin, Germany",
        "description": "Food delivery platform",
        "scrape_frequency": "daily"
    },
    {
        "name": "N26",
        "career_url": "https://n26.com/en/careers",
        "industry": "Fintech",
        "size": "1000-5000",
        "location": "Berlin, Germany",
        "description": "Digital banking",
        "scrape_frequency": "weekly"
    },
    {
        "name": "Celonis",
        "career_url": "https://www.celonis.com/careers/",
        "industry": "Enterprise Software",
        "size": "1000-5000",
        "location": "Munich, Germany",
        "description": "Process mining software",
        "scrape_frequency": "weekly"
    },
    {
        "name": "TeamViewer",
        "career_url": "https://www.teamviewer.com/en/company/careers/",
        "industry": "Software",
        "size": "1000-5000",
        "location": "Göppingen, Germany",
        "description": "Remote connectivity software",
        "scrape_frequency": "weekly"
    },
]


def seed_companies():
    """Seed the companies table with German companies"""
    print("🌱 Seeding companies database...")
    
    # Initialize database
    init_db()
    
    db = SessionLocal()
    
    try:
        # Check if already seeded
        existing_count = db.query(Company).count()
        if existing_count > 0:
            print(f"ℹ️  Database already contains {existing_count} companies")
            response = input("Do you want to add more companies? (y/n): ")
            if response.lower() != 'y':
                print("Skipping seed.")
                return
        
        added_count = 0
        
        for company_data in GERMAN_COMPANIES:
            # Check if company already exists
            existing = db.query(Company).filter(Company.name == company_data["name"]).first()
            
            if existing:
                print(f"  ⏭️  {company_data['name']} already exists, skipping")
                continue
            
            # Create new company
            company = Company(**company_data)
            db.add(company)
            added_count += 1
            print(f"  ✅ Added {company_data['name']}")
        
        db.commit()
        
        total = db.query(Company).count()
        print(f"\n✅ Seeding complete!")
        print(f"   Added: {added_count} companies")
        print(f"   Total: {total} companies in database")
        
    except Exception as e:
        print(f"❌ Error seeding companies: {e}")
        db.rollback()
    
    finally:
        db.close()


if __name__ == "__main__":
    seed_companies()
