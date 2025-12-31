# 📊 Match Score System & Scraping Explained

## 🎯 How Match Scores Work (60%, 70%, 80%)

### What is a Match Score?

**Match Score** is an AI-calculated percentage (0-100%) showing how well a job matches YOUR profile based on:

1. **Skills Match** (40 points)
   - Your resume skills vs. job requirements
   - Example: You have Python, SQL, Docker → Job needs Python, SQL, Kubernetes
   - Match: 66% (2 out of 3)

2. **Experience Level** (20 points)
   - Your years of experience vs. job's requirement
   - Example: You have 5 years → Job wants 3-7 years = Perfect match

3. **Keywords Density** (20 points)
   - How many of your resume keywords appear in the job description
   - More matches = Higher score

4. **Salary Alignment** (10 points)
   - Your expected salary vs. offered salary
   - Within range = High score

5. **Location/Remote Preference** (10 points)
   - Your location preferences vs. job location
   - Remote job when you want remote = Perfect match

### Match Score Ranges:

| Score | Badge Color | Meaning | Action |
|-------|-------------|---------|--------|
| 80-100% | 🟢 Green | **Excellent Match** | Apply immediately! |
| 70-79% | 🟡 Yellow | **Good Match** | Strong candidate, apply |
| 60-69% | 🟠 Orange | **Fair Match** | Consider if interested |
| Below 60% | 🔴 Red | **Low Match** | Skills gap exists |

### How the Filter Buttons Work:

When you click **"80%+ Match"**:
- Shows ONLY jobs where AI calculated ≥80% match
- These are your BEST opportunities
- High chance of getting interviews

When you click **"70%+ Match"**:
- Shows jobs with ≥70% match
- Still very good opportunities
- You meet most requirements

When you click **"60%+ Match"**:
- Shows all jobs with ≥60% match
- Worth considering if you're learning

### Why Jobs Disappeared When You Clicked 60/70/80%?

**Problem**: The original 50 demo jobs didn't have match scores calculated.
**Solution**: I've now updated the seed script to automatically create match scores!

**To fix and see jobs again:**

```bash
# 1. Clear old jobs without scores
curl -X DELETE http://localhost:8000/api/dev/clear-all-jobs

# 2. Seed new jobs WITH match scores
curl -X POST "http://localhost:8000/api/dev/seed-demo-jobs?count=50"

# 3. Refresh your browser
```

Now when you click 60%/70%/80% buttons, you'll see jobs!

## 🚀 How Scraping Works (Behind the Scenes)

### When You Click "Start New Scrape":

#### Step 1: **You Enter**:
- Keyword: "Python Developer"
- Location: "Berlin"
- Sources: (Select from dropdown)

#### Step 2: **Backend Process** (happens automatically):

```
1. Scraper Manager receives your request
   ↓
2. Connects to selected job boards (Kimeta, Indeed, LinkedIn, etc.)
   ↓
3. Searches each board for "Python Developer" in "Berlin"
   ↓
4. Extracts job data:
   - Title, Company, Location
   - Salary, Job Type, Remote options
   - Full description
   - Requirements, Benefits
   - Application URL
   ↓
5. Normalizes data (different boards have different formats)
   ↓
6. Checks for duplicates (same job on multiple boards)
   ↓
7. Saves unique jobs to database
   ↓
8. **AI Analysis** (if API keys configured):
   - Analyzes job description
   - Extracts key skills
   - Calculates match score against your profile
   - Generates ATS score
   - Creates interview questions
   - Suggests resume improvements
   ↓
9. Jobs appear in your dashboard with match scores
```

#### Step 3: **What You See**:
- 50-100+ new jobs appear
- Each has a match score badge
- Filters update automatically
- Analytics charts refresh

### Scraping Sources Currently Working:

#### ✅ **Implemented** (Ready to use now):
1. **Arbeitsagentur** - German Federal Agency (no API needed)
2. **Kimeta** - Aggregator (scrapes 20+ boards at once!)
3. **Joblift** - Meta-search (another aggregator)
4. **Jooble** - Job search engine
5. **Indeed** (via JobSpy library)
6. **LinkedIn** (via JobSpy library)
7. **StepStone** (via JobSpy library)
8. **Glassdoor** (via JobSpy library)

#### 🔧 **Configured** (Can be added):
All the German boards you listed:
- GermanTechJobs, Honeypot, Jobvector, Gulp, 4Scotty
- Berlin Startup Jobs, Arbeitnow, EnglishJobs.de
- Experteer, Monster.de, XING Jobs
- And 30+ more!

### Which Sources Are Preferred?

**For SPEED** (Quick scan):
```
Kimeta + Joblift + Indeed
```
These 3 aggregators already pull from 50+ smaller boards!

**For TECH JOBS**:
```
LinkedIn + StepStone + GermanTechJobs + Honeypot + Stack Overflow
```

**For STARTUPS** (English-speaking):
```
Berlin Startup Jobs + Arbeitnow + EnglishJobs.de + The Local
```

**For COMPREHENSIVE** (everything):
```
Arbeitsagentur + Kimeta + Indeed + LinkedIn + StepStone + XING
```

### How to Configure Scraping:

#### Option 1: **Via Frontend UI** (Easiest):
1. Click "Start New Scrape"
2. Enter keyword: "Data Scientist"
3. Enter location: "Munich"
4. Select sources from dropdown
5. Click "Start"
6. Wait 30-60 seconds
7. Jobs appear automatically!

#### Option 2: **Via API** (Advanced):
```bash
curl -X POST "http://localhost:8000/api/scrapers/scrape?keyword=DevOps%20Engineer&location=Hamburg&sources=kimeta&sources=indeed&sources=linkedin"
```

#### Option 3: **Automatic Scheduled** (Set it and forget it):
Edit `backend/utils/scheduler.py`:
```python
# Run scraping every day at 8 AM
scheduler.add_job(
    func=daily_scrape,
    trigger='cron',
    hour=8,
    minute=0,
)
```

## 🤖 AI Analysis Features (Requires API Keys)

### With Gemini API Key:

Once you add your Gemini API key, each scraped job gets:

1. **Match Score Calculation**
   - Compares job requirements vs. your skills
   - Returns 0-100% compatibility score

2. **ATS Score Analysis**
   - Checks if your resume will pass Applicant Tracking Systems
   - Identifies missing keywords
   - Formatting score

3. **Interview Questions**
   - Generates 10-15 likely interview questions
   - Technical + Behavioral + Company-specific

4. **Resume Tailoring**
   - Rewrites your resume bullets to match the job
   - Optimizes keywords for ATS
   - Highlights relevant experience

5. **Missing Skills Detection**
   - Shows what skills you need to learn
   - Prioritizes most important gaps

### With Perplexity API:

Can be used for:
- Company research
- Industry trends
- Salary benchmarking
- Market insights

### How to Enable AI Features:

1. **Add API keys to .env**:
```env
GEMINI_API_KEY=your_actual_gemini_key_here
PERPLEXITY_API_KEY=your_perplexity_key_here
```

2. **Restart backend**:
```bash
sudo docker compose restart backend
```

3. **Scrape new jobs** - AI analysis happens automatically!

4. **View analysis** - Click any job card to see full AI insights

## 🔍 Understanding the Companies List

You provided 50+ German job boards. Here's how they're organized:

### **Aggregators** (Scrape these first!):
- **Kimeta** - Pulls from 20+ smaller boards
- **Joblift** - Meta-search across 15+ sources  
- **Indeed** - Aggregates 30+ sources
- **Jooble** - Combines smaller regional boards

**👉 Benefit**: One scrape = 20+ boards covered!

### **Direct Job Boards**:
- StepStone, Monster, Arbeitsagentur, XING
- Each has unique jobs not on aggregators
- Usually higher quality postings

### **Niche Boards** (Target specific):
- **Tech**: GermanTechJobs, Honeypot, Stack Overflow
- **Startups**: Berlin Startup Jobs, Arbeitnow
- **Finance**: eFinancialCareers
- **Creative**: Dasauge

### **Regional Boards**:
- Bayern, Berlin, Hamburg-specific boards
- Often have jobs missed by big platforms
- Good for local opportunities

## 🛠️ Fixing the Clear Button Issue

**Problem**: Clear button wasn't resetting filters properly.

**Fix Applied**: Updated `clearAllFilters()` function to:
- Reset all filters to empty
- Clear search term
- Reset to page 1
- Trigger data refetch

**Test it**:
1. Apply some filters (Source: LinkedIn, Type: Full-time)
2. Click "Clear" button
3. All filters should reset
4. All 50 jobs should appear again

## 📊 Current Status & Next Steps

### ✅ What's Working Now:
- 50 demo jobs with match scores
- Match score filters (60%, 70%, 80%)
- Clear filters button fixed
- 8 scraping sources active
- AI analysis configured (needs API keys)

### 🔄 To See Jobs with Match Scores:

Run these commands:

```bash
# Clear old jobs
curl -X DELETE http://localhost:8000/api/dev/clear-all-jobs

# Seed new jobs WITH match scores  
curl -X POST "http://localhost:8000/api/dev/seed-demo-jobs?count=50"

# Check it worked
curl -s "http://localhost:8000/api/jobs?limit=3" | python3 -m json.tool
```

Then refresh http://localhost:3000 and click 80%+ filter!

### 🚀 To Start Real Scraping:

1. Create `.env` file with your API keys
2. Restart backend
3. Click "Start New Scrape"
4. Enter: Keyword="Python Developer", Location="Berlin"
5. Wait 30 seconds
6. See real jobs appear!

---

**Questions? Check these endpoints:**

- All sources: http://localhost:8000/api/scrapers/sources
- Database stats: http://localhost:8000/api/dev/stats  
- API docs: http://localhost:8000/docs
