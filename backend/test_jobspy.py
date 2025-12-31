from jobspy import scrape_jobs

print("Testing JobSpy scraper...")
try:
    jobs_df = scrape_jobs(
        site_name=["indeed", "linkedin"],
        search_term="Machine Learning Engineer",
        location="Berlin, Germany",
        results_wanted=5,
        hours_old=168
    )
    print(f"Found {len(jobs_df)} jobs")
    if len(jobs_df) > 0:
        for i, row in jobs_df.head(3).iterrows():
            print(f"\nJob {i+1}:")
            print(f"  Title: {row.get('title', 'N/A')}")
            print(f"  Company: {row.get('company', 'N/A')}")
            print(f"  URL: {row.get('job_url', 'N/A')}")
    else:
        print("No jobs found!")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
