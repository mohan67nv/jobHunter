# 🐳 Starting SmartJobHunter Pro with Docker

## Docker Permission Issue - Easy Fix

Docker needs permission to run. Here are two options:

---

## Option 1: Use sudo (Quick & Easy)

Just add `sudo` before docker commands:

```bash
# Start with Docker (one command)
sudo docker compose up --build

# Or start in background
sudo docker compose up --build -d

# View logs
sudo docker compose logs -f

# Stop
sudo docker compose down
```

**That's it!** This works immediately.

---

## Option 2: Fix Permissions (One-time setup)

Run these commands once to use Docker without sudo:

```bash
# Add your user to docker group
sudo usermod -aG docker $USER

# Apply the changes
newgrp docker

# Test (should work without sudo now)
docker compose up --build -d
```

**Note**: You may need to log out and log back in for this to take full effect.

---

## 🚀 Quick Start (Choose One Method)

### Method A: With sudo
```bash
sudo docker compose up --build
```

### Method B: Without Docker (Manual)

**Terminal 1 - Backend:**
```bash
cd backend
source jobHunter/bin/activate
uvicorn app:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm install
npm run dev
```

---

## 🌐 Access Your App

After starting (wait 1-2 minutes):

- **Frontend**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs
- **Health**: http://localhost:8000/health

---

## ✅ Current Status

✅ **Docker**: Installed (needs sudo)
✅ **Python env**: jobHunter (52 packages)
✅ **Database**: Created (8 tables, 15 companies)
✅ **API Keys**: Gemini ✅ | Perplexity ✅
✅ **Code**: Complete and ready

---

## 🎯 Recommended: Start with sudo

**Easiest way to start right now:**

```bash
sudo docker compose up --build
```

Then visit http://localhost:3000 after 1-2 minutes!

---

## 📚 What's Next

1. **Start the app** (with sudo or manual method)
2. **Visit** http://localhost:3000
3. **Upload** your resume in Settings
4. **Set** preferences (keywords, locations)
5. **Start** scraping jobs
6. **Get** AI match scores!

---

**You're ready to go!** 🚀
