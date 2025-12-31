"""
Developer utilities and debugging endpoints
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.job import Job
from datetime import datetime, timedelta
import random

router = APIRouter(prefix="/api/dev", tags=["developer"])


@router.post("/seed-demo-jobs")
def seed_demo_jobs(count: int = 50, db: Session = Depends(get_db)):
    """Seed database with demo jobs for UI testing"""
    
    companies = [
        "Google Germany", "SAP", "BMW Group", "Siemens", "Deutsche Bank",
        "Zalando", "N26", "HelloFresh", "Delivery Hero", "Auto1 Group",
        "Lufthansa", "Bosch", "Mercedes-Benz", "Volkswagen", "Allianz",
        "Adidas", "Porsche", "Infineon", "BASF", "Bayer"
    ]
    
    job_titles = [
        "Senior Python Developer", "Data Scientist", "ML Engineer", 
        "Full Stack Developer", "DevOps Engineer", "Backend Developer",
        "AI Research Scientist", "Software Architect", "Technical Lead",
        "Frontend Developer (React)", "Cloud Engineer", "Data Engineer",
        "Security Engineer", "Product Manager", "QA Engineer"
    ]
    
    locations = [
        "Berlin", "Munich", "Hamburg", "Frankfurt", "Cologne",
        "Stuttgart", "Düsseldorf", "Leipzig", "Dresden", "Bonn",
        "Hannover", "Remote - Germany", "Hybrid - Munich", "Hybrid - Berlin"
    ]
    
    sources = [
        "LinkedIn", "Indeed", "StepStone", "Glassdoor", 
        "Xing", "Arbeitsagentur", "Kimeta", "Joblift", "Jooble", "Monster"
    ]
    
    job_types = ["Full-time", "Part-time", "Contract", "Freelance", "Internship"]
    remote_types = ["Remote", "Hybrid", "On-site"]
    experience_levels = ["Entry Level", "Mid Level", "Senior", "Lead", "Executive"]
    
    description_template = """We are looking for a talented {title} to join our innovative team!

🎯 Key Responsibilities:
• Design and develop scalable, high-performance applications
• Collaborate with cross-functional teams (Product, Design, QA)
• Write clean, maintainable, and well-documented code
• Participate in code reviews and technical discussions
• Mentor junior developers and share knowledge
• Contribute to architectural decisions
• Optimize application performance and scalability

✅ Requirements:
• {exp_years}+ years of experience in software development
• Strong programming skills in Python, Java, JavaScript, or Go
• Experience with cloud platforms (AWS, Azure, or GCP)
• Proficiency with modern development tools (Git, Docker, CI/CD)
• Excellent problem-solving and analytical abilities
• Strong communication skills and team collaboration
• Experience with Agile/Scrum methodologies
• Bachelor's degree in Computer Science or related field

🌟 Nice to Have:
• Experience with microservices architecture
• Knowledge of Kubernetes and container orchestration
• Contributions to open-source projects
• Experience with machine learning or data engineering
• Certifications (AWS, Azure, GCP)

💰 Benefits:
• Competitive salary (€{salary_min}k - €{salary_max}k)
• Flexible working hours and remote work options
• €2,000 annual learning budget for courses and conferences
• Modern tech stack and latest tools
• Comprehensive health insurance
• Company pension plan (bAV)
• 30 days vacation + special leave days
• Team events and company outings
• Relocation support for international candidates
• Gym membership or sports budget
• Free snacks, drinks, and lunches
• Career growth opportunities

🚀 Our Tech Stack:
Python, Django/FastAPI, React, TypeScript, PostgreSQL, Redis, Docker, Kubernetes, AWS/GCP, GitLab CI/CD, Terraform

📍 Location: {location}
🏢 Work Model: {remote_type}
"""
    
    jobs_created = 0
    
    for i in range(count):
        exp_years = random.randint(2, 7)
        salary_min = random.randint(45, 85)
        salary_max = salary_min + random.randint(15, 35)
        title = random.choice(job_titles)
        location = random.choice(locations)
        remote_type = random.choice(remote_types)
        
        description = description_template.format(
            title=title.lower(),
            exp_years=exp_years,
            salary_min=salary_min,
            salary_max=salary_max,
            location=location,
            remote_type=remote_type
        )
        
        job = Job(
            title=title,
            company=random.choice(companies),
            location=location,
            source=random.choice(sources),
            url=f"https://careers.example.com/job/{random.randint(10000, 99999)}",
            description=description,
            requirements="Python, SQL, Git, Docker, Kubernetes, CI/CD, REST APIs, Agile, TDD",
            benefits="Health Insurance, Remote Work, Learning Budget, Pension Plan, Flexible Hours",
            salary=f"€{salary_min}k - €{salary_max}k",
            job_type=random.choice(job_types),
            contract_type="Permanent" if random.random() > 0.2 else "Contract",
            remote_type=remote_type,
            experience_level=random.choice(experience_levels),
            posted_date=datetime.now() - timedelta(days=random.randint(0, 45)),
            is_active=True,
            is_duplicate=False,
        )
        db.add(job)
        db.flush()  # Get job.id
        
        # Create analysis with match score
        from models.job import JobAnalysis
        import json
        match_score = random.randint(55, 98)
        analysis = JobAnalysis(
            job_id=job.id,
            match_score=match_score,
            ats_score=random.randint(60, 95),
            matching_skills=json.dumps(["Python", "SQL", "Git", "Docker"]),
            missing_skills=json.dumps(["Kubernetes", "Terraform"]),
            experience_match="Close" if match_score > 75 else "Gap",
            salary_match="Match",
            keyword_density=random.randint(40, 85),
        )
        db.add(analysis)
        jobs_created += 1
    
    db.commit()
    
    total = db.query(Job).filter(Job.is_active == True).count()
    
    return {
        "message": "Demo jobs seeded successfully",
        "jobs_created": jobs_created,
        "total_jobs_in_db": total
    }


@router.delete("/clear-all-jobs")
def clear_all_jobs(db: Session = Depends(get_db)):
    """Delete all jobs from database (dev only)"""
    deleted = db.query(Job).delete()
    db.commit()
    return {"message": "All jobs deleted", "count": deleted}


@router.get("/stats")
def get_database_stats(db: Session = Depends(get_db)):
    """Get database statistics"""
    total_jobs = db.query(Job).count()
    active_jobs = db.query(Job).filter(Job.is_active == True).count()
    
    sources_count = db.query(Job.source, db.func.count(Job.id)).group_by(Job.source).all()
    
    return {
        "total_jobs": total_jobs,
        "active_jobs": active_jobs,
        "sources": [{"source": s, "count": c} for s, c in sources_count]
    }
