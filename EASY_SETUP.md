# 🚀 EASY SETUP - SmartJobHunter Pro

## The Simplest Way to Get Started (Using Docker)

Since we're having issues with C compilers, **let's use Docker instead!** Docker has everything pre-installed and configured.

---

## ✅ Quick Steps

### Step 1: Get Your API Key (2 minutes)

1. Go to: **https://makersuite.google.com/app/apikey**
2. Sign in with Google
3. Click **"Create API Key"**
4. Copy the key (looks like: `AIzaSyD...`)

### Step 2: Add API Key to .env (1 minute)

The `.env` file has been created. Now edit it:

```bash
# Open in your favorite editor
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

**Save the file!**

### Step 3: Start with Docker (1 minute)

```bash
# Build and start everything
docker-compose up --build
```

That's it! Wait 1-2 minutes for Docker to build and start.

### Step 4: Access the Application

Open your browser:
- **Dashboard**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs

---

## 🎯 What to Do First

Once the app is running:

1. **Go to Settings** (top right)
2. **Upload your resume** (Profile tab - PDF, DOCX, or TXT)
3. **Set preferences** (Preferences tab):
   - Keywords: "Data Scientist", "Python", "Machine Learning"
   - Locations: "Munich", "Berlin", "Remote"
   - Salary: 60000 (€60k minimum)
4. **Go back to Dashboard**
5. **Click "Start Scraping"** button
6. Wait 30-60 seconds for jobs to appear
7. **Click on any job** to see AI analysis!

---

## 🔧 Common Commands

```bash
# Start the application
docker-compose up

# Start in background (detached mode)
docker-compose up -d

# Stop the application
docker-compose down

# View logs
docker-compose logs -f

# Rebuild after code changes
docker-compose up --build

# Check if containers are running
docker-compose ps
```

---

## 🧪 Test Your Setup

### Test 1: Check if Docker is running
```bash
docker-compose ps
```

You should see:
- `jobhunter_backend` - running
- `jobhunter_frontend` - running

### Test 2: Check API
```bash
curl http://localhost:8000/health
```

Should return: `{"status":"healthy",...}`

### Test 3: Check Frontend
Open: http://localhost:3000

You should see the SmartJobHunter dashboard!

---

## 🐛 Troubleshooting

### Problem: "Port already in use"

```bash
# Stop any existing containers
docker-compose down

# Kill processes on ports
lsof -ti:8000 | xargs kill -9  # Backend port
lsof -ti:3000 | xargs kill -9  # Frontend port

# Try again
docker-compose up
```

### Problem: "Cannot connect to Docker daemon"

```bash
# Start Docker
sudo systemctl start docker

# Or restart Docker Desktop (on Mac/Windows)
```

### Problem: "API Key not working"

1. Make sure you edited `.env` (not `.env.example`)
2. Check that there are no spaces around the `=`
3. Restart Docker: `docker-compose down && docker-compose up`

### Problem: "No jobs appearing"

1. Check that you added your API key
2. Try manual scrape: 
   ```bash
   curl -X POST "http://localhost:8000/api/scrapers/scrape?keyword=Data%20Scientist&location=Germany"
   ```
3. Check logs: `docker-compose logs backend`

---

## 📦 What Docker Does For You

Docker automatically:
- ✅ Installs ALL required packages
- ✅ Sets up the database
- ✅ Configures everything
- ✅ Runs the backend (FastAPI)
- ✅ Runs the frontend (React)
- ✅ Handles all dependencies

No need to worry about:
- ❌ C compilers
- ❌ System libraries
- ❌ Python versions
- ❌ Package conflicts

---

## 🎓 Understanding the Setup

### What's Running?

When you run `docker-compose up`, you get:

1. **Backend Container** (Python + FastAPI)
   - Port 8000
   - All Python packages installed
   - Database included
   - AI agents ready

2. **Frontend Container** (React + TypeScript)
   - Port 3000
   - Beautiful UI
   - Connected to backend

### Where's the Data?

All your data is saved in:
- `data/jobhunter.db` - Your database (SQLite)
- `data/resumes/` - Uploaded resumes
- `data/exports/` - Generated files
- `logs/` - Application logs

These folders are **on your computer**, not in Docker! So your data is safe even if you stop Docker.

---

## 🚀 Next Steps After Setup

### 1. Upload Your Resume
Go to Settings → Profile → Upload Resume

### 2. Run First Scrape
Dashboard → "Start Scraping" → Wait 30-60 seconds

### 3. Explore Features
- Click on jobs to see AI match scores
- View Analytics page for charts
- Track applications as you apply

### 4. Customize
- Add more companies in Settings
- Adjust scraping preferences
- Set up notifications (optional)

---

## 💡 Pro Tips

1. **Run in background**: Use `docker-compose up -d` to run detached
2. **Check logs anytime**: `docker-compose logs backend -f`
3. **Stop gracefully**: Always use `docker-compose down` (not Ctrl+C multiple times)
4. **Backup your data**: The `data/` folder contains everything important
5. **Update code**: After changes, run `docker-compose up --build`

---

## ✅ Summary

| What | Status | How |
|------|--------|-----|
| Docker Setup | ✅ | `docker-compose up` |
| API Key | ⚠️ | **Add to .env file** |
| Database | ✅ | Auto-created by Docker |
| Packages | ✅ | Auto-installed by Docker |
| Frontend | ✅ | Auto-started by Docker |
| Backend | ✅ | Auto-started by Docker |

---

## 🎯 You're Ready!

**Right now, just do 2 things:**

1. ✅ Add your Gemini API key to `.env`
2. ✅ Run `docker-compose up`

That's all! The application will start automatically.

Visit http://localhost:3000 and start your job hunt! 🚀

---

**Need help?** Check the logs: `docker-compose logs -f`
