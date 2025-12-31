# Scheduler Service Setup

## Overview
The scheduler service automates:
1. **Daily Job Scraping** - Runs twice daily (8 AM & 6 PM)
2. **Match Score Calculation** - Runs every 2 hours for new jobs

## Installation

### 1. Install Dependencies
```bash
docker exec jobhunter_backend pip install schedule==1.2.0
```

### 2. Run Scheduler Service

#### Option A: Run in Background (Production)
```bash
# Start scheduler as background service
docker exec -d jobhunter_backend python3 /app/scheduler_service.py
```

#### Option B: Run in Foreground (Development/Testing)
```bash
# View logs in real-time
docker exec -it jobhunter_backend python3 /app/scheduler_service.py
```

#### Option C: Add to Docker Compose (Recommended)
Add scheduler service to `docker-compose.yml`:

```yaml
services:
  scheduler:
    build: ./backend
    container_name: jobhunter_scheduler
    command: python3 /app/scheduler_service.py
    volumes:
      - ./backend:/app
      - ./data:/app/data
    environment:
      - GOOGLE_API_KEY=${GOOGLE_API_KEY}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - PERPLEXITY_API_KEY=${PERPLEXITY_API_KEY}
    depends_on:
      - backend
    restart: unless-stopped
```

Then start:
```bash
docker-compose up -d scheduler
```

## Configuration

### Customize Schedule
Edit `/backend/scheduler_service.py`:

```python
# Current schedule
schedule.every().day.at("08:00").do(run_daily_scraping)  # 8 AM
schedule.every().day.at("18:00").do(run_daily_scraping)  # 6 PM
schedule.every(2).hours.do(calculate_match_scores)      # Every 2 hours

# Change to custom times:
schedule.every().day.at("06:00").do(run_daily_scraping)  # 6 AM
schedule.every().day.at("20:00").do(run_daily_scraping)  # 8 PM
schedule.every(1).hours.do(calculate_match_scores)      # Every 1 hour
```

### Customize Search Keywords
Set keywords in Profile Settings:
- Go to Settings → Profile
- Add keywords: "Python Developer, Data Scientist, ML Engineer"
- Save

The scheduler will use these keywords for automated scraping.

## Monitoring

### Check Scheduler Logs
```bash
# View live logs
docker logs -f jobhunter_backend | grep "Scheduler"

# Or if running as separate service
docker logs -f jobhunter_scheduler
```

### Check Scraping Results
```bash
# Check latest scraping activity
docker exec jobhunter_backend python3 -c "
from database import SessionLocal
from models.scraping_log import ScrapingLog
from sqlalchemy import desc

db = SessionLocal()
logs = db.query(ScrapingLog).order_by(desc(ScrapingLog.completed_at)).limit(5).all()

for log in logs:
    print(f'{log.source}: {log.jobs_new} new jobs, {log.status}')
"
```

## Stopping the Scheduler

### If Running in Background
```bash
# Find process
docker exec jobhunter_backend ps aux | grep scheduler_service

# Kill process
docker exec jobhunter_backend pkill -f scheduler_service.py
```

### If Running as Service
```bash
docker stop jobhunter_scheduler
```

## Troubleshooting

### Issue: No jobs being scraped
**Solution**: Check if user profile has search keywords set:
```bash
docker exec jobhunter_backend python3 -c "
from database import SessionLocal
from models.user import User

db = SessionLocal()
user = db.query(User).first()
print(f'Keywords: {user.search_keywords if user else \"No user profile\"}')
"
```

### Issue: Match scores not calculating
**Solution**: Ensure user profile exists with skills:
- Go to Settings → Profile
- Add skills to your profile
- Save and wait for next calculation cycle (runs every 2 hours)

### Issue: Scheduler not running
**Solution**: Check logs for errors:
```bash
docker logs --tail 100 jobhunter_backend 2>&1 | grep -E "(ERROR|Exception)"
```

## Quick Test

Run manual scraping and match score calculation:
```bash
# Test scraping
docker exec jobhunter_backend python3 -c "
from scheduler_service import run_daily_scraping
run_daily_scraping()
"

# Test match scoring
docker exec jobhunter_backend python3 -c "
from scheduler_service import calculate_match_scores
calculate_match_scores()
"
```
