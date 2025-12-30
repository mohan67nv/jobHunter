# 🐳 Docker Guide - SmartJobHunter Pro

## Why Docker is Perfect for This Project

✅ **Portability**: Move to new laptop in seconds
✅ **No Dependencies**: Everything bundled in containers
✅ **Consistency**: Works exactly the same everywhere
✅ **Easy Backup**: Copy the folder and you're done
✅ **No Setup**: No Python, Node.js, or package installation needed

---

## 🚀 Quick Start with Docker

### 1. Make Sure Your API Key is Set

Edit `.env` file (you already did this!):
```bash
GEMINI_API_KEY=AIzaSyD[your-actual-key]
OPENAI_API_KEY=sk-[your-chatgpt-key]  # Add when you get it
PERPLEXITY_API_KEY=pplx-[your-key]    # Add when you get it
ROVO_API_KEY=[your-rovo-key]          # Add when you get it
```

### 2. Start Everything with One Command

```bash
docker compose up --build
```

That's it! Docker will:
- Build the backend container with all Python packages
- Build the frontend container with all Node packages
- Create the database
- Start both servers
- Connect them together

**First time takes 3-5 minutes. After that, starts in 10 seconds!**

### 3. Access Your Application

- **Frontend Dashboard**: http://localhost:3000
- **API Documentation**: http://localhost:8000/docs
- **API Health**: http://localhost:8000/health

---

## 📦 What Docker Gives You

### Backend Container
- Python 3.11 with all 52 packages
- FastAPI web server
- SQLite database (auto-created)
- All scrapers configured
- AI agents ready (multi-provider)
- Scheduler running

### Frontend Container
- Node.js 20 with React 18
- All npm packages installed
- Vite dev server
- Hot reload enabled
- Beautiful UI ready

### Automatic Features
- Database persistence (data/ folder)
- Log persistence (logs/ folder)
- Hot reload for code changes
- Auto-restart on crash
- Port forwarding configured

---

## 🔧 Common Docker Commands

### Start the Application
```bash
# Start and see logs
docker compose up

# Start in background (detached mode)
docker compose up -d

# Rebuild and start (after code changes)
docker compose up --build
```

### Stop the Application
```bash
# Stop containers
docker compose down

# Stop and remove everything (keeps data/)
docker compose down --volumes
```

### View Logs
```bash
# All logs
docker compose logs -f

# Backend only
docker compose logs -f backend

# Frontend only
docker compose logs -f frontend

# Last 100 lines
docker compose logs --tail=100
```

### Check Status
```bash
# See running containers
docker compose ps

# See resource usage
docker stats
```

### Access Container Shell
```bash
# Backend shell
docker compose exec backend bash

# Frontend shell
docker compose exec frontend sh
```

### Restart Services
```bash
# Restart everything
docker compose restart

# Restart backend only
docker compose restart backend
```

---

## 📂 Moving to New Laptop (Super Easy!)

### Method 1: Copy the Folder
```bash
# On old laptop - create backup
tar -czf smartjobhunter-backup.tar.gz smartjobhunter/

# Copy to new laptop (USB/cloud/network)
# On new laptop - extract
tar -xzf smartjobhunter-backup.tar.gz
cd smartjobhunter

# Start immediately!
docker compose up -d
```

**That's it!** Your data, settings, and everything transfers perfectly.

### Method 2: Git Repository
```bash
# On old laptop
cd smartjobhunter
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-git-repo>
git push

# On new laptop
git clone <your-git-repo>
cd smartjobhunter
docker compose up -d
```

**Note**: The `data/` folder with your database will need to be copied separately if not in git.

---

## 🔄 What Persists When You Move

### ✅ Automatically Saved
- Database: `data/jobhunter.db` (all your jobs and applications)
- Uploaded resumes: `data/resumes/`
- Generated files: `data/exports/`
- Logs: `logs/`
- Configuration: `.env` file

### ⚠️ Need to Copy
- `.env` file (contains your API keys)
- `data/` folder (your database and files)
- `logs/` folder (if you want history)

### 🔄 Docker Rebuilds Automatically
- Python packages
- Node packages
- Containers

---

## 🎯 Multi-AI Provider Setup

Your setup supports multiple AI providers for different purposes!

### Primary (Gemini Pro)
```bash
GEMINI_API_KEY=AIzaSyD...  # ✅ You already set this
```
**Use for**: Job analysis, resume matching (FREE, 60 req/min)

### ChatGPT/OpenAI (When you add it)
```bash
OPENAI_API_KEY=sk-proj-...
```
**Use for**: Complex reasoning, cover letter generation
**Cost**: ~$0.01-0.03 per job analysis

### Perplexity (When you add it)
```bash
PERPLEXITY_API_KEY=pplx-...
```
**Use for**: Company research, real-time web search
**Cost**: Pay per use

### Anthropic Claude (When you add it)
```bash
ANTHROPIC_API_KEY=sk-ant-...
```
**Use for**: Long-form content, detailed analysis
**Cost**: Pay per use

### RovoDev (When you add it)
```bash
ROVO_API_KEY=...
```
**Use for**: Development assistance, code generation

### How Multi-Provider Works
The app automatically:
1. Tries Gemini first (fastest, free)
2. Falls back to Claude if Gemini fails
3. Falls back to OpenAI if Claude fails
4. Uses Perplexity for web searches
5. Uses RovoDev for development tasks

**You only need Gemini to start!** Add others later for enhanced features.

---

## 💾 Backup Strategy

### Quick Backup (Essential Files Only)
```bash
# Backup just your data
tar -czf backup-data-$(date +%Y%m%d).tar.gz data/ .env

# Restore
tar -xzf backup-data-20240130.tar.gz
```

### Full Backup (Everything)
```bash
# Backup entire project
cd ..
tar -czf smartjobhunter-full-$(date +%Y%m%d).tar.gz smartjobhunter/

# Restore
tar -xzf smartjobhunter-full-20240130.tar.gz
```

### Automated Backup (Add to crontab)
```bash
# Backup data daily at 2 AM
0 2 * * * cd /path/to/smartjobhunter && tar -czf ../backups/data-$(date +\%Y\%m\%d).tar.gz data/ .env
```

---

## 🐛 Troubleshooting Docker

### Port Already in Use
```bash
# Stop other services
docker compose down

# Or change ports in docker-compose.yml
# frontend: "3001:3000"  (use 3001 instead)
# backend: "8001:8000"   (use 8001 instead)
```

### Database Issues
```bash
# Restart with fresh database
docker compose down
rm data/jobhunter.db
docker compose up --build
```

### Container Won't Start
```bash
# Check logs
docker compose logs backend
docker compose logs frontend

# Rebuild from scratch
docker compose down
docker compose build --no-cache
docker compose up
```

### Out of Disk Space
```bash
# Clean up old images
docker system prune -a

# Remove unused volumes
docker volume prune
```

---

## 🎓 Docker vs Manual Setup

### With Docker (Recommended)
✅ Start: `docker compose up`
✅ Move: Copy folder
✅ No setup needed
✅ Same environment everywhere
✅ 5 minutes to get running

### Without Docker (What you did before)
❌ Install Python, Node.js, packages
❌ Activate environments
❌ Manage dependencies
❌ Different on each machine
❌ 30+ minutes to setup

---

## 📊 Resource Usage

Typical Docker resource usage:
- **RAM**: ~500MB (backend) + ~300MB (frontend) = 800MB
- **Disk**: ~2GB for images + your data
- **CPU**: Low (idle), Medium (scraping), High (AI analysis)

**Your laptop can easily handle this!**

---

## ✅ Checklist for New Laptop

When you get your new laptop:

- [ ] Install Docker Desktop
- [ ] Copy `smartjobhunter` folder
- [ ] Check `.env` has your API keys
- [ ] Run `docker compose up -d`
- [ ] Visit http://localhost:3000
- [ ] Done! 🎉

**Estimated time: 5 minutes**

---

## 🎯 Summary

### Current Status
✅ Docker installed
✅ Docker Compose configured
✅ Backend Dockerfile ready
✅ Frontend Dockerfile ready
✅ docker-compose.yml configured
✅ .env file with Gemini API key
✅ Frontend packages installed (500+)
✅ Backend packages in Docker image

### Ready to Use
```bash
docker compose up --build
```

### Ready to Move
Just copy the folder to new laptop and run the same command!

---

**You're all set for easy development and seamless migration!** 🚀
