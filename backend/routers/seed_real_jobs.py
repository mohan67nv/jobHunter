"""
Seed realistic ML/AI jobs matched to user's resume
Based on actual resume: Senior ML Engineer with Python, PyTorch, Federated Learning, MLOps
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.job import Job, JobAnalysis
from datetime import datetime, timedelta
import random

router = APIRouter(prefix="/api/seed", tags=["seed"])


REALISTIC_ML_JOBS = [
    {
        "title": "Senior Machine Learning Engineer - Federated Learning",
        "company": "Bosch AI Lab",
        "location": "Berlin, Germany",
        "salary": "€80,000 - €110,000",
        "job_type": "full-time",
        "remote_type": "hybrid",
        "experience_level": "senior",
        "source": "LinkedIn",
        "url": "https://www.linkedin.com/jobs/view/3789456123",
        "description": "Join our AI Lab to build privacy-preserving ML systems using Federated Learning. Work with PyTorch and Flower framework to deploy models across distributed edge devices.",
        "requirements": "• 4+ years ML engineering experience\n• Expert in Python, PyTorch, TensorFlow\n• Hands-on Federated Learning experience (Flower/PySyft)\n• MLOps: Docker, Kubernetes, MLFlow\n• GDPR compliance and Privacy-by-Design",
        "benefits": "• Flexible hybrid work\n• €3000 education budget\n• 30 days vacation\n• Company pension",
        "match_score": 96
    },
    {
        "title": "MLOps Engineer - Azure Cloud Infrastructure",
        "company": "Siemens Energy",
        "location": "Munich, Germany",
        "salary": "€75,000 - €100,000",
        "job_type": "full-time",
        "remote_type": "hybrid",
        "experience_level": "mid-senior",
        "source": "StepStone",
        "url": "https://www.stepstone.de/stellenangebote/mlops-engineer-azure-siemens-12345678.html",
        "description": "Build scalable MLOps pipelines on Azure for energy optimization. Work with IoT data, time series forecasting, and production ML deployment.",
        "requirements": "• Strong Python and ML frameworks\n• Azure: Databricks, Data Factory, Synapse\n• CI/CD: Jenkins, GitLab, Terraform\n• Time series forecasting (LSTM/RNN)\n• Docker, Kubernetes orchestration",
        "benefits": "• Remote-first culture\n• Stock options\n• Health insurance\n• Public transport pass",
        "match_score": 94
    },
    {
        "title": "AI Engineer - Privacy & Decentralized ML",
        "company": "SAP AI Research",
        "location": "Berlin, Germany",
        "salary": "€85,000 - €115,000",
        "job_type": "full-time",
        "remote_type": "hybrid",
        "experience_level": "senior",
        "source": "Indeed",
        "url": "https://de.indeed.com/viewjob?jk=sap-ai-berlin-789xyz",
        "description": "Research and implement differential privacy and federated learning solutions. Collaborate with cross-functional teams to deploy GDPR-compliant AI systems.",
        "requirements": "• MSc/PhD in CS/Data Science\n• Federated Learning expertise\n• Differential Privacy, PySyft knowledge\n• Python, PyTorch, TensorFlow Lite\n• Strong research background",
        "benefits": "• Flexible working hours\n• Conference budget €5000/year\n• Relocation support\n• Modern office in Berlin Mitte",
        "match_score": 93
    },
    {
        "title": "Machine Learning Engineer - IoT & Edge AI",
        "company": "Viessmann Climate Solutions",
        "location": "Frankfurt, Germany",
        "salary": "€70,000 - €95,000",
        "job_type": "full-time",
        "remote_type": "hybrid",
        "experience_level": "mid-senior",
        "source": "Glassdoor",
        "url": "https://www.glassdoor.com/job-listing/machine-learning-engineer-viessmann-JV_IC2762618.htm?jl=1009123456",
        "description": "Deploy ML models on resource-constrained IoT devices for smart heating systems. Work with TensorFlow Lite, Home Assistant, and edge computing.",
        "requirements": "• 3+ years ML engineering\n• TensorFlow Lite, MQTT, InfluxDB\n• IoT and edge deployment experience\n• Docker containerization\n• Energy/HVAC domain knowledge (plus)",
        "benefits": "• 30 vacation days\n• Company car option\n• Fitness membership\n• Team events",
        "match_score": 91
    },
    {
        "title": "Senior Data Scientist - Time Series & Optimization",
        "company": "E.ON Digital Technology",
        "location": "Hamburg, Germany",
        "salary": "€72,000 - €98,000",
        "job_type": "full-time",
        "remote_type": "remote",
        "experience_level": "senior",
        "source": "Joblift",
        "url": "https://joblift.de/eon-data-scientist",
        "description": "Build forecasting models for energy demand prediction. Apply mathematical optimization and operations research to grid management.",
        "requirements": "• Strong Python, NumPy, Pandas\n• Time series: LSTM, RNN, ARIMA\n• Mathematical Optimization (MILP, Linear Programming)\n• Big Data: Spark, Azure\n• Energy sector experience preferred",
        "benefits": "• 100% remote possible\n• MacBook Pro\n• €2000 learning budget\n• Private health insurance",
        "match_score": 89
    },
    {
        "title": "Machine Learning Engineer - Production ML Systems",
        "company": "Zalando SE",
        "location": "Berlin, Germany",
        "salary": "€75,000 - €105,000",
        "job_type": "full-time",
        "remote_type": "hybrid",
        "experience_level": "mid-senior",
        "source": "LinkedIn",
        "url": "https://linkedin.com/zalando-ml-production",
        "description": "Scale ML systems to millions of users. Build recommendation engines and search ranking models in production environment.",
        "requirements": "• Python expert (5+ years)\n• Production ML: Kubernetes, Docker, Airflow\n• ML frameworks: PyTorch, Scikit-learn\n• Monitoring: Prometheus, Grafana\n• Agile/Scrum experience",
        "benefits": "• Relocation package €5000\n• Learning budget €3000/year\n• Free lunch daily\n• Zalando discount 40%",
        "match_score": 87
    },
    {
        "title": "AI/ML Engineer - Computer Vision & NLP",
        "company": "BMW Group",
        "location": "Munich, Germany",
        "salary": "€78,000 - €108,000",
        "job_type": "full-time",
        "remote_type": "hybrid",
        "experience_level": "senior",
        "source": "StepStone",
        "url": "https://stepstone.de/bmw-ai-engineer",
        "description": "Develop autonomous driving perception systems. Work on object detection, semantic segmentation, and sensor fusion using deep learning.",
        "requirements": "• Deep Learning: PyTorch, TensorFlow\n• Computer Vision: OpenCV, YOLO, Mask R-CNN\n• GPU programming, CUDA\n• C++ and Python proficiency\n• Automotive domain knowledge (plus)",
        "benefits": "• Company car (electric)\n• Profit sharing bonus\n• 35-hour work week\n• On-site gym and cafeteria",
        "match_score": 85
    },
    {
        "title": "MLOps Platform Engineer",
        "company": "Deutsche Telekom IT",
        "location": "Bonn, Germany",
        "salary": "€68,000 - €92,000",
        "job_type": "full-time",
        "remote_type": "hybrid",
        "experience_level": "mid-level",
        "source": "Kimeta",
        "url": "https://kimeta.de/telekom-mlops",
        "description": "Build internal MLOps platform to accelerate ML development across the organization. Terraform infrastructure as code, CI/CD pipelines.",
        "requirements": "• Strong Python development\n• Kubernetes, Docker expertise\n• Terraform, GitLab CI/CD\n• MLFlow, Kubeflow, or similar\n• Cloud: AWS or Azure",
        "benefits": "• 38-hour week\n• Generous pension plan\n• Mobile and internet free\n• Career development programs",
        "match_score": 84
    },
    {
        "title": "Data Scientist - NLP & Generative AI",
        "company": "Axel Springer SE",
        "location": "Berlin, Germany",
        "salary": "€65,000 - €90,000",
        "job_type": "full-time",
        "remote_type": "hybrid",
        "experience_level": "mid-level",
        "source": "Indeed",
        "url": "https://indeed.com/axel-springer-nlp",
        "description": "Build NLP pipelines for automated content analysis and generation. Work with LLMs, sentiment analysis, and text classification.",
        "requirements": "• Python, NLP libraries (spaCy, NLTK)\n• Transformer models, BERT, GPT\n• ML: Scikit-learn, PyTorch\n• SQL, data pipelines\n• German language (B2+)",
        "benefits": "• Flexible hours\n• Modern Berlin office\n• Free magazines/newspapers\n• Team lunches weekly",
        "match_score": 82
    },
    {
        "title": "Senior ML Engineer - Recommender Systems",
        "company": "Delivery Hero",
        "location": "Berlin, Germany",
        "salary": "€80,000 - €110,000",
        "job_type": "full-time",
        "remote_type": "remote",
        "experience_level": "senior",
        "source": "Glassdoor",
        "url": "https://glassdoor.com/delivery-hero-ml-recsys",
        "description": "Design and deploy real-time recommendation engines at scale. Work with A/B testing, personalization, and ranking algorithms.",
        "requirements": "• 5+ years ML engineering\n• Recommender systems experience\n• Python, Spark, Kafka\n• Real-time ML serving\n• Distributed systems knowledge",
        "benefits": "• Fully remote worldwide\n• Stock options\n• €4000 home office budget\n• Annual company retreat",
        "match_score": 86
    },
    {
        "title": "Machine Learning Engineer - FinTech",
        "company": "N26 Bank",
        "location": "Berlin, Germany",
        "salary": "€75,000 - €105,000",
        "job_type": "full-time",
        "remote_type": "hybrid",
        "experience_level": "mid-senior",
        "source": "LinkedIn",
        "url": "https://linkedin.com/n26-ml-fintech",
        "description": "Build fraud detection and risk scoring models. Real-time ML inference, anomaly detection, and financial forecasting.",
        "requirements": "• Python, ML frameworks\n• Fraud detection, anomaly detection\n• Real-time ML systems\n• Kafka, microservices\n• Financial domain knowledge (plus)",
        "benefits": "• N26 Black account free\n• Learning budget €2000\n• International team\n• Berlin tech hub office",
        "match_score": 83
    },
    {
        "title": "AI Research Engineer - Reinforcement Learning",
        "company": "Bosch Center for AI",
        "location": "Renningen, Germany",
        "salary": "€70,000 - €95,000",
        "job_type": "full-time",
        "remote_type": "on-site",
        "experience_level": "mid-senior",
        "source": "StepStone",
        "url": "https://stepstone.de/bosch-rl-research",
        "description": "Research and develop RL algorithms for robotics and autonomous systems. Publish in top-tier conferences.",
        "requirements": "• MSc/PhD in ML/Robotics\n• Reinforcement Learning expertise\n• Python, PyTorch, OpenAI Gym\n• Research publications\n• Strong math background",
        "benefits": "• Research freedom\n• Conference travel budget\n• Collaboration with universities\n• Bosch pension scheme",
        "match_score": 79
    },
    {
        "title": "Data Scientist - Healthcare AI",
        "company": "Siemens Healthineers",
        "location": "Erlangen, Germany",
        "salary": "€68,000 - €93,000",
        "job_type": "full-time",
        "remote_type": "hybrid",
        "experience_level": "mid-level",
        "source": "Jooble",
        "url": "https://jooble.de/siemens-healthineers-ds",
        "description": "Develop ML models for medical imaging analysis. Work with CNNs for disease detection and diagnostic support systems.",
        "requirements": "• Python, TensorFlow/PyTorch\n• Medical imaging, Computer Vision\n• Data privacy, regulatory compliance\n• Statistics and experimentation\n• Healthcare domain interest",
        "benefits": "• Impact on healthcare\n• 30 days vacation\n• Professional development\n• Hybrid 3 days/week",
        "match_score": 81
    },
    {
        "title": "ML Platform Engineer - Kubernetes",
        "company": "Contentful",
        "location": "Berlin, Germany",
        "salary": "€72,000 - €100,000",
        "job_type": "full-time",
        "remote_type": "remote",
        "experience_level": "mid-senior",
        "source": "LinkedIn",
        "url": "https://linkedin.com/contentful-ml-platform",
        "description": "Build scalable ML infrastructure on Kubernetes. Enable data scientists with self-service ML tools and automated deployment.",
        "requirements": "• Kubernetes expert\n• Python, Go programming\n• ML frameworks integration\n• Terraform, Helm charts\n• AWS or GCP experience",
        "benefits": "• Remote-first company\n• €3000 learning budget\n• Latest tech equipment\n• Quarterly team meetups",
        "match_score": 85
    },
    {
        "title": "Senior Python Developer - ML Infrastructure",
        "company": "Celonis",
        "location": "Munich, Germany",
        "salary": "€75,000 - €105,000",
        "job_type": "full-time",
        "remote_type": "hybrid",
        "experience_level": "senior",
        "source": "Glassdoor",
        "url": "https://glassdoor.com/celonis-python-ml",
        "description": "Build data pipelines and ML infrastructure for process mining. High-performance Python, distributed systems, and big data processing.",
        "requirements": "• Expert Python (5+ years)\n• Distributed systems\n• Apache Spark, Kafka\n• ML pipeline orchestration\n• Performance optimization",
        "benefits": "• Stock options\n• €4000 education budget\n• Munich Oktoberfest party\n• Flexible vacation",
        "match_score": 84
    }
]


@router.post("/seed-ml-jobs")
def seed_realistic_ml_jobs(db: Session = Depends(get_db)):
    """Seed realistic ML/AI jobs matched to user's resume"""
    
    # Clear existing jobs first
    db.query(JobAnalysis).delete()
    db.query(Job).delete()
    db.commit()
    
    created_count = 0
    
    for job_data in REALISTIC_ML_JOBS:
        # Create job
        posted_days_ago = random.randint(1, 14)
        job = Job(
            title=job_data["title"],
            company=job_data["company"],
            location=job_data["location"],
            url=job_data["url"],
            source=job_data["source"],
            description=job_data["description"],
            requirements=job_data["requirements"],
            benefits=job_data["benefits"],
            salary=job_data["salary"],
            job_type=job_data["job_type"],
            remote_type=job_data["remote_type"],
            experience_level=job_data["experience_level"],
            posted_date=datetime.now() - timedelta(days=posted_days_ago),
            is_active=True
        )
        db.add(job)
        db.flush()
        
        # Create job analysis with match score
        analysis = JobAnalysis(
            job_id=job.id,
            match_score=job_data["match_score"],
            ats_score=random.randint(75, 95),
            matching_skills="Python, PyTorch, Machine Learning, MLOps, Docker, Kubernetes",
            missing_skills="Domain-specific knowledge varies by role",
            recommendations="Strong match based on your Federated Learning and MLOps experience. Apply immediately.",
            analyzed_at=datetime.now()
        )
        db.add(analysis)
        created_count += 1
    
    db.commit()
    
    return {
        "message": "✅ Seeded realistic ML/AI jobs matched to your resume",
        "jobs_created": created_count,
        "match_scores": "79% - 96%",
        "locations": "Berlin, Munich, Hamburg, Frankfurt, Bonn, Erlangen",
        "companies": "Bosch, Siemens, SAP, BMW, Zalando, N26, Delivery Hero, and more",
        "note": "Jobs are realistic and matched to your Senior ML Engineer profile with Federated Learning, PyTorch, MLOps skills"
    }
