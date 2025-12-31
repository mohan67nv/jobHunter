# 🚀 Real Job Scraping Setup Guide

## ✅ Current Status

Your application now has **50 demo jobs** loaded! Refresh http://localhost:3000 to see them.

## 📊 What You Can Do Now

1. **Browse Jobs**: See all 50 jobs with filters
2. **Test Filters**: Filter by source, job type, location, experience
3. **View Details**: Click on any job to see full details
4. **Test Analytics**: Go to Analytics page to see charts
5. **Test Interview Prep**: Navigate to Interview Prep section

## 🎯 Next Step: Real Scraping with API Keys

### Step 1: Create .env File

```bash
cd /home/mohana-ga/MNVProjects/jobHunter
cp .env.example .env
nano .env  # or use any text editor
```

### Step 2: Add Your API Keys

Edit the `.env` file with your actual API keys:

```env
# AI API Keys (for job analysis and matching)
GEMINI_API_KEY=your_actual_gemini_api_key_here
ANTHROPIC_API_KEY=your_actual_anthropic_key (optional)
OPENAI_API_KEY=your_actual_openai_key (optional)

# Security (generate a random string)
SECRET_KEY=generate_with_python_command_below

# Web Scraping
USER_AGENT=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36

# Email & Telegram (optional for notifications)
EMAIL_HOST=smtp.gmail.com
EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
EMAIL_FROM=your_email@gmail.com

TELEGRAM_BOT_TOKEN=optional
TELEGRAM_CHAT_ID=optional
```

### Step 3: Generate SECRET_KEY

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

Copy the output and paste it as SECRET_KEY in .env

### Step 4: Restart Backend with .env

```bash
cd /home/mohana-ga/MNVProjects/jobHunter
sudo docker compose restart backend
```

Wait 10 seconds for backend to fully start.

### Step 5: Test Real Scraping

#### Option A: Via Frontend UI
1. Go to http://localhost:3000
2. Click "Start New Scrape" button
3. Enter keyword: "Python Developer"
4. Enter location: "Berlin"
5. Select sources (LinkedIn, Indeed, etc.)
6. Click "Start Scraping"

#### Option B: Via API
```bash
curl -X POST "http://localhost:8000/api/scrapers/scrape?keyword=Data%20Scientist&location=Munich&sources=arbeitsagentur"
```

### Step 6: Check Scraping Progress

```bash
# View backend logs
sudo docker compose logs backend --tail=50 -f

# Check job count
curl -s "http://localhost:8000/api/dev/stats" | python3 -m json.tool
```

## 🔍 Scraping Sources Available

### Currently Configured:
1. **Arbeitsagentur** - German federal employment agency (no API key needed)
2. **Kimeta** - Job aggregator (works without API)
3. **Joblift** - German job board (web scraping)
4. **Jooble** - International job search engine

### With JobSpy Library (requires python-jobspy):
5. **LinkedIn** - Professional network
6. **Indeed** - World's largest job site
7. **StepStone** - Leading German job portal
8. **Glassdoor** - Jobs + company reviews

## 🤖 AI-Powered Features (Requires API Keys)

### With Gemini API:
- **Job Analysis**: Analyze job descriptions
- **Skill Matching**: Match your skills to job requirements
- **ATS Score**: Calculate resume compatibility
- **Interview Questions**: Generate role-specific questions
- **Resume Tailoring**: Optimize resume for specific jobs

### How It Works:
1. Jobs are scraped from multiple sources
2. AI analyzes each job description
3. Matches against your profile/resume
4. Generates insights and recommendations
5. Creates interview prep materials

## 📝 Scraping Configuration

### Customize Scraping Behavior:

Edit `backend/scrapers/scraper_manager.py`:

```python
# Change number of results
results_wanted=100  # Increase/decrease

# Change scraping frequency
# Edit backend/utils/scheduler.py
scheduler.add_job(
    func=scheduled_scrape,
    trigger='cron',
    hour=8,  # Run at 8 AM
    minute=0,
)
```

## 🎨 UI Visualization Tips

Now that you have data loaded:

### 1. Dashboard View
- **Gradient Cards**: Show total jobs, new today, avg match
- **Filters**: Test all filter combinations
- **Match Score Badges**: Color-coded (red/yellow/green)
- **Quick Filters**: 60%, 70%, 80%+ buttons

### 2. Job Detail Modal
- Click any job card
- See full description
- View requirements and benefits
- Check ATS score section (once AI is configured)

### 3. Analytics Page
- **Charts**: View job distribution by source
- **Timeline**: See when jobs were posted
- **Export**: Download data as CSV
- **Skills**: See most demanded skills

### 4. Applications Tracking
Navigate to Applications page and:
- Click "Track Application" on any job
- Choose status (Applied/Interview/Offer)
- Add notes
- Track progress

## 🔧 Useful Developer Commands

### Seed More Demo Jobs
```bash
curl -X POST "http://localhost:8000/api/dev/seed-demo-jobs?count=100"
```

### Clear All Jobs
```bash
curl -X DELETE "http://localhost:8000/api/dev/clear-all-jobs"
```

### Check Database Stats
```bash
curl -s "http://localhost:8000/api/dev/stats" | python3 -m json.tool
```

### View Scraping History
```bash
curl -s "http://localhost:8000/api/scrapers/history" | python3 -m json.tool
```

### Test Specific Scraper
```bash
# Test Arbeitsagentur only
curl -X POST "http://localhost:8000/api/scrapers/scrape?keyword=Software%20Engineer&location=Berlin&sources=arbeitsagentur"

# Test multiple sources
curl -X POST "http://localhost:8000/api/scrapers/scrape?keyword=DevOps&location=Hamburg&sources=kimeta&sources=joblift"
```

## 🚨 Troubleshooting Scraping

### Issue: "0 jobs found"
**Possible causes:**
1. Website structure changed (scrapers need update)
2. Rate limiting (too many requests)
3. IP blocked (use VPN or rotate IPs)
4. Keyword/location mismatch

**Solutions:**
- Try different keywords
- Use broader location ("Germany" instead of specific city)
- Wait a few hours between scraping runs
- Check backend logs for errors

### Issue: "ImportError: python-jobspy not installed"
```bash
sudo docker compose exec backend pip install python-jobspy
sudo docker compose restart backend
```

### Issue: API keys not working
1. Verify .env file exists: `ls -la .env`
2. Check format (no spaces around =)
3. Restart backend: `sudo docker compose restart backend`
4. Check logs: `sudo docker compose logs backend | grep API`

## 📈 Next Improvements

### UI Enhancements (based on data visualization):
1. **Salary Charts**: Visualize salary ranges
2. **Company Insights**: Show top hiring companies
3. **Location Heatmap**: Map view of job locations
4. **Skill Cloud**: Word cloud of required skills
5. **Application Funnel**: Conversion rate tracking

### Feature Additions:
1. **Email Alerts**: Get notified of new matching jobs
2. **Telegram Bot**: Receive updates via Telegram
3. **Auto-Apply**: Automatically apply to matching jobs
4. **Resume Optimizer**: AI-powered resume improvements
5. **Interview Scheduler**: Calendar integration

### Scraping Improvements:
1. **Company Career Pages**: Direct scraping from BMW, SAP, etc.
2. **Xing Integration**: German professional network
3. **Monster.de**: Another major job board
4. **Freelance Platforms**: Upwork, Fiverr for freelance gigs

## 🎉 You're Ready!

1. ✅ Frontend working with beautiful UI
2. ✅ Backend API functional
3. ✅ 50 demo jobs loaded
4. ✅ All filters and features working
5. 📝 Next: Add your API keys for real scraping

**Open http://localhost:3000 now and explore your fully functional job hunting platform!**

---

Need help? Check:
- Backend API docs: http://localhost:8000/docs
- Frontend console: Press F12 in browser
- Backend logs: `sudo docker compose logs backend -f`
