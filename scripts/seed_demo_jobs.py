"""
Seed demo jobs for testing UI
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from datetime import datetime, timedelta
import random
from database import SessionLocal
from models.job import Job

def seed_demo_jobs():
    """Create demo jobs for UI testing"""
    db = SessionLocal()
    
    companies = [
        "Google Germany", "SAP", "BMW Group", "Siemens", "Deutsche Bank",
        "Zalando", "N26", "HelloFresh", "Delivery Hero", "Auto1 Group",
        "Lufthansa", "Bosch", "Mercedes-Benz", "Volkswagen", "Allianz"
    ]
    
    job_titles = [
        "Senior Python Developer", "Data Scientist", "ML Engineer", 
        "Full Stack Developer", "DevOps Engineer", "Backend Developer",
        "AI Research Scientist", "Software Architect", "Technical Lead",
        "Frontend Developer", "Cloud Engineer", "Data Engineer"
    ]
    
    locations = [
        "Berlin", "Munich", "Hamburg", "Frankfurt", "Cologne",
        "Stuttgart", "Düsseldorf", "Leipzig", "Dresden", "Remote"
    ]
    
    sources = [
        "LinkedIn", "Indeed", "StepStone", "Glassdoor", 
        "Xing", "Arbeitsagentur", "Kimeta", "Joblift"
    ]
    
    job_types = ["Full-time", "Part-time", "Contract", "Freelance"]
    remote_types = ["Remote", "Hybrid", "On-site"]
    experience_levels = ["Entry Level", "Mid Level", "Senior", "Lead", "Executive"]
    
    descriptions = [
        """We are looking for a talented developer to join our team. 

Key Responsibilities:
• Design and develop scalable applications
• Collaborate with cross-functional teams
• Write clean, maintainable code
• Participate in code reviews
• Mentor junior developers

Requirements:
• 3+ years of experience in software development
• Strong programming skills in Python/Java/JavaScript
• Experience with cloud platforms (AWS/Azure/GCP)
• Excellent problem-solving abilities
• Strong communication skills

Benefits:
• Competitive salary
• Remote work options
• Learning budget
• Health insurance
• Modern tech stack""",
        
        """Join our innovative team and shape the future of technology!

What you'll do:
• Build cutting-edge applications
• Work with latest technologies
• Solve challenging problems
• Contribute to open source
• Drive technical decisions

What we need:
• Deep technical expertise
• Passion for technology
• Team player mindset
• Continuous learner
• Strong analytical skills

What we offer:
• Flexible working hours
• Professional development
• Great team culture
• Stock options
• Relocation support""",
    ]
    
    print("🌱 Seeding demo jobs...")
    
    jobs_created = 0
    for i in range(50):
        job = Job(
            title=random.choice(job_titles),
            company=random.choice(companies),
            location=random.choice(locations),
            source=random.choice(sources),
            url=f"https://example.com/job/{i}",
            description=random.choice(descriptions),
            requirements="Python, SQL, Git, Docker, Kubernetes, CI/CD",
            benefits="Health Insurance, Flexible Hours, Remote Work, Learning Budget",
            salary=f"€{random.randint(50, 120)}k - €{random.randint(70, 150)}k",
            job_type=random.choice(job_types),
            contract_type="Permanent" if random.random() > 0.3 else "Contract",
            remote_type=random.choice(remote_types),
            experience_level=random.choice(experience_levels),
            posted_date=datetime.now() - timedelta(days=random.randint(0, 30)),
            match_score=random.randint(60, 98),
            is_active=True,
        )
        db.add(job)
        jobs_created += 1
    
    db.commit()
    print(f"✅ Created {jobs_created} demo jobs")
    
    # Verify
    total = db.query(Job).count()
    print(f"📊 Total jobs in database: {total}")
    
    db.close()

if __name__ == "__main__":
    seed_demo_jobs()
