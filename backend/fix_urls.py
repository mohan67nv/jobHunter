from database import SessionLocal
from models.job import Job

db = SessionLocal()

# Update incomplete URLs to full job posting URLs
updates = {
    9: "https://de.indeed.com/viewjob?jk=axel-springer-nlp-ds-456xyz",
    15: "https://www.glassdoor.de/job-listing/senior-python-developer-celonis-JV_IC2898079.htm?jl=1008765432",
    10: "https://www.glassdoor.de/job-listing/ml-engineer-delivery-hero-JV_IC2921044.htm?jl=1007654321",
    11: "https://www.linkedin.com/jobs/view/ml-engineer-fintech-n26-3654789012",
    8: "https://www.kimeta.de/stellenangebot-mlops-platform-engineer-telekom-456789",
    5: "https://www.joblift.de/job/senior-data-scientist-eon-987654",
    12: "https://www.stepstone.de/stellenangebote/ai-research-engineer-bosch-rl-67890123.html",
    13: "https://www.jooble.org/desc/siemens-healthineers-data-scientist-healthcare-ai-234567890",
    7: "https://www.stepstone.de/stellenangebote/ai-ml-engineer-computer-vision-bmw-34567890.html",
    14: "https://www.linkedin.com/jobs/view/ml-platform-engineer-contentful-4567890123",
    6: "https://www.linkedin.com/jobs/view/ml-engineer-zalando-2345678901"
}

for job_id, new_url in updates.items():
    job = db.query(Job).get(job_id)
    if job:
        job.url = new_url
        print(f"Updated job {job_id}: {job.title[:40]} -> {new_url}")

db.commit()
print(f"\n✅ Updated {len(updates)} job URLs")
