# 🚀 Quick Start Guide

## ✅ Setup Complete!

Your SmartJobHunter Pro is ready. Package conflicts have been fixed!

---

## 🚀 Start the Application

### Method 1: Use the startup script (Easiest)
```bash
cd jobHunter
./start.sh
```

### Method 2: Manual commands
```bash
cd jobHunter
sudo docker compose build
sudo docker compose up -d
```

**Wait 30-60 seconds for services to fully start.**

---

## 🌐 Access Your Application

After starting:

- **Frontend Dashboard**: http://localhost:3000
- **API Documentation**: http://localhost:8000/docs  
- **Health Check**: http://localhost:8000/health

---

## 🔧 Useful Commands

```bash
# View logs (all services)
sudo docker compose logs -f

# View backend logs only
sudo docker compose logs -f backend

# View frontend logs only
sudo docker compose logs -f frontend

# Check status
sudo docker compose ps

# Stop the application
./stop.sh
# or
sudo docker compose down

# Restart
sudo docker compose restart
```

---

## 🎯 First Steps After Starting

1. **Visit the Dashboard**: http://localhost:3000

2. **Upload Your Resume**:
   - Click "Settings" (top right)
   - Go to "Profile" tab
   - Upload your PDF/DOCX resume
   - AI will extract skills automatically

3. **Set Preferences**:
   - In Settings → "Preferences" tab
   - Add keywords: "Data Scientist", "Python", "Machine Learning"
   - Add locations: "Munich", "Berlin", "Remote"
   - Set minimum salary: 60000

4. **Start Scraping**:
   - Go back to "Dashboard"
   - Click "Start Scraping" button
   - Wait 30-60 seconds
   - Jobs will appear with AI match scores!

5. **View Job Analysis**:
   - Click on any job card
   - See AI match score (0-100%)
   - View matching/missing skills
   - Get recommendations

---

## 🤖 Your AI Setup

Currently active:
- ✅ **Gemini Pro** (FREE, primary AI)
- ✅ **Perplexity** (web search & research)

Ready to add:
- ⏳ **ChatGPT** (when you add API key)
- ⏳ **Claude** (when you add API key)
- ⏳ **RovoDev** (when you add API key)

---

## 📂 Moving to New Laptop

1. Copy entire `jobHunter` folder to new laptop
2. Run: `./start.sh`
3. Done! Everything works immediately.

---

## 🐛 Troubleshooting

### Services won't start
```bash
sudo docker compose down
sudo docker compose up --build -d
```

### Check if services are running
```bash
sudo docker compose ps
```

### View error logs
```bash
sudo docker compose logs backend
sudo docker compose logs frontend
```

### Port already in use
```bash
# Stop any existing containers
sudo docker compose down

# Or check what's using the port
sudo lsof -i :8000  # Backend
sudo lsof -i :3000  # Frontend
```

---

## ✅ What Was Fixed

- ✅ Package version conflicts resolved
- ✅ httpx version made compatible with all AI providers
- ✅ python-telegram-bot version flexibility added
- ✅ Ready for all AI providers (Gemini, ChatGPT, Claude, Perplexity, RovoDev)

---

## 🎉 You're Ready!

Run: `./start.sh`

Then visit: http://localhost:3000

Happy job hunting! 🚀
