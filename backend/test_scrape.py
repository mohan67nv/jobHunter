from python_jobspy import scrape_jobs
import sys

print("Testing JobSpy scraper...")
try:
    jobs_df = scrape_jobs(
        site_name="indeed",
        search_term="Machine Learning",
        location="Berlin, Germany",
        results_wanted=5,
        hours_old=168
    )
    print(f"✅ Scraped {len(jobs_df)} jobs")
    if len(jobs_df) > 0:
        print(f"\nFirst job: {jobs_df.iloc[0]['title']} at {jobs_df.iloc[0]['company']}")
        print(f"URL: {jobs_df.iloc[0]['job_url']}")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
