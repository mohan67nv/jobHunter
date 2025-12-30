# 🎯 START HERE - SmartJobHunter Pro

## ✅ Installation Complete!

Your SmartJobHunter Pro is **READY TO USE**!

---

## 📦 What's Installed

✅ **Python Environment**: `jobHunter` virtual environment
✅ **All Core Packages**: FastAPI, SQLAlchemy, Gemini AI, BeautifulSoup, etc.
✅ **Database**: SQLite with 8 tables created
✅ **Project Files**: Complete backend and frontend code

---

## 🔑 STEP 1: Get Your FREE Gemini API Key (2 minutes)

1. Go to: **https://makersuite.google.com/app/apikey**
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Click **"Create API key in new project"**
5. **Copy the key** (looks like: `AIzaSyD...`)

### Why Gemini?
- ✅ **FREE** to use
- ✅ **60 requests/minute** (plenty for job hunting)
- ✅ **No credit card required**
- ✅ **Best AI for text analysis**

---

## 🔧 STEP 2: Add Your API Key (1 minute)

Open the `.env` file that's already created:

```bash
# Use your favorite editor
nano .env
# or
code .env
# or
vim .env
```

**Find this line:**
```
GEMINI_API_KEY=your_gemini_key_here
```

**Replace with your actual key:**
```
GEMINI_API_KEY=AIzaSyDxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**SAVE THE FILE!** (In nano: Ctrl+X, then Y, then Enter)

---

## 🚀 STEP 3: Start the Application (30 seconds)

### Start Backend:

```bash
cd backend
source jobHunter/bin/activate
uvicorn app:app --reload --host 0.0.0.0
```

**You should see:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

### Test Backend:
Open in browser: **http://localhost:8000/docs**

You should see the API documentation page!

---

## 🎨 STEP 4: Start the Frontend (Optional)

**Open a NEW terminal window:**

```bash
cd frontend
npm install
npm run dev
```

Then visit: **http://localhost:3000**

---

## 🎯 STEP 5: Use the Application

### Option A: Use the Web Dashboard (if frontend is running)

1. **Go to Settings** → Profile
2. **Upload your resume** (PDF, DOCX, or TXT)
3. **Set preferences** → Keywords, locations
4. **Go to Dashboard**
5. **Click "Start Scraping"**
6. **View AI-analyzed jobs!**

### Option B: Use the API Directly

**1. Test API Health:**
```bash
curl http://localhost:8000/health
```

**2. Create User Profile:**
```bash
curl -X GET http://localhost:8000/api/user/profile
```

**3. Trigger Job Scraping:**
```bash
curl -X POST "http://localhost:8000/api/scrapers/scrape?keyword=Data%20Scientist&location=Germany"
```

**4. List Jobs:**
```bash
curl http://localhost:8000/api/jobs
```

**5. Analyze a Job:**
```bash
curl -X POST http://localhost:8000/api/analysis/analyze-job/1
```

---

## 📚 Quick Reference

### Activate Environment
```bash
cd backend
source jobHunter/bin/activate
```

### Start Backend
```bash
cd backend
source jobHunter/bin/activate
uvicorn app:app --reload
```

### Start Frontend
```bash
cd frontend
npm install
npm run dev
```

### View Logs
```bash
tail -f logs/jobhunter.log
```

### Initialize Database (if needed)
```bash
cd backend
source jobHunter/bin/activate
python -c "from database import init_db; init_db()"
```

### Seed Companies (optional)
```bash
cd backend
source jobHunter/bin/activate
python scripts/seed_companies.py
```

---

## 🌐 Access URLs

- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **API Health**: http://localhost:8000/health
- **Frontend Dashboard**: http://localhost:3000 (if running)

---

## ✅ Verification Checklist

Run these commands to verify everything works:

```bash
# 1. Check Python environment
cd backend && source jobHunter/bin/activate && python --version

# 2. Check packages
cd backend && source jobHunter/bin/activate && pip list | grep -E "(fastapi|sqlalchemy|google-generativeai)"

# 3. Check database
ls -lh data/jobhunter.db

# 4. Check API key (after adding to .env)
cd backend && source jobHunter/bin/activate && python -c "from dotenv import load_dotenv; import os; load_dotenv('../.env'); print('✅ API Key found!' if os.getenv('GEMINI_API_KEY') and 'your_gemini' not in os.getenv('GEMINI_API_KEY') else '❌ Add your real API key to .env')"

# 5. Start backend
cd backend && source jobHunter/bin/activate && uvicorn app:app --reload
```

---

## 🎓 What Each Component Does

### Backend (Port 8000)
- **FastAPI**: Web framework for API
- **SQLAlchemy**: Database management
- **Gemini AI**: Analyzes jobs and resumes
- **Beautiful Soup**: Scrapes job websites
- **APScheduler**: Runs automated scraping

### Frontend (Port 3000)
- **React**: User interface
- **TypeScript**: Type-safe code
- **Tailwind CSS**: Beautiful styling
- **Charts**: Visual analytics

### Database
- **SQLite**: Stores all your data
- **Location**: `data/jobhunter.db`
- **8 Tables**: Jobs, Applications, Analysis, etc.

---

## 💡 Pro Tips

1. **Always activate the environment** before running Python commands:
   ```bash
   cd backend && source jobHunter/bin/activate
   ```

2. **Check logs** if something doesn't work:
   ```bash
   tail -f logs/jobhunter.log
   ```

3. **API Documentation** is your friend:
   http://localhost:8000/docs

4. **Test endpoints** in the browser before coding

5. **Backup your data** (the `data/` folder)

---

## 🐛 Troubleshooting

### "Module not found" error
```bash
cd backend
source jobHunter/bin/activate
pip install -r requirements-simple.txt
```

### "Port already in use"
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9
```

### "Database locked"
```bash
# Close all database connections
# Restart the backend
```

### "API key not working"
1. Make sure you edited `.env` (not `.env.example`)
2. No spaces around the `=` sign
3. Key should start with `AIza`
4. Restart the backend after editing

---

## 📖 Documentation

- **This file**: Quick start guide
- **README.md**: Complete documentation
- **API_KEYS_SETUP.md**: Detailed API key guide
- **INSTALLATION_COMPLETE.md**: Installation details
- **API Docs**: http://localhost:8000/docs (when running)

---

## 🎯 Summary

**Right now, you only need to do 2 things:**

1. ✅ **Add your Gemini API key** to `.env` file
2. ✅ **Start the backend**: `cd backend && source jobHunter/bin/activate && uvicorn app:app --reload`

Then visit: **http://localhost:8000/docs**

**That's all!** 🚀

The frontend is optional - you can use the API directly through the documentation page.

---

**Questions?** Check the troubleshooting section or the full README.md

**Happy job hunting!** 🎉
