# 🎯 QUICK START GUIDE

## Build & Run (Choose One Method)

### Method 1: Using the build script (Recommended for Docker issues)
```bash
cd /home/mohana-ga/MNVProjects/jobHunter
./build.sh
```

### Method 2: Using the start script
```bash
cd /home/mohana-ga/MNVProjects/jobHunter
./start.sh
```

### Method 3: Manual Docker commands
```bash
cd /home/mohana-ga/MNVProjects/jobHunter
sudo docker compose down
sudo docker compose build --no-cache
sudo docker compose up -d
```

---

## 🌐 Access URLs

After successful build:

- **Frontend (Main App)**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

---

## 📱 Quick Feature Tour

### 1. Dashboard (/)
- View all scraped jobs
- Use advanced filters (Source, Job Type, Location, Experience, Date)
- Click "Start New Scrape" to fetch new jobs
- Quick filter by match score (60%, 70%, 80%+)
- Click any job to see details + ATS analysis

### 2. Compare CV-JD (/compare)
- Paste your CV on the left
- Paste Job Description on the right
- Click "Analyze with AI"
- View match score and recommendations

### 3. Applications (/applications)
- Track all your applications
- Update status (Applied → Phone Screen → Interview → Offer)
- Set interview dates
- Add notes

### 4. Interview Prep (/interview-prep)
- Only shows jobs with "Interview" status
- Select a job from left sidebar
- View AI-generated questions categorized:
  - Technical (coding, algorithms)
  - Behavioral (STAR method)
  - Company-specific
- Expand questions to add notes
- Mark questions as "prepared"

### 5. Analytics (/analytics)
- View job statistics
- Match score distribution
- Jobs by source
- Application funnel
- Top companies
- Skills demand trends
- Export any chart to CSV
- Export all data with one click

### 6. Resume Manager (/resumes)
- Create multiple resume versions
- Track which version used for which application

### 7. Templates (/templates)
- Manage resume and cover letter templates
- Edit and customize

### 8. Settings (/settings)
- Upload your default resume
- Set preferences
- Configure AI analysis settings

---

## 🔄 Common Operations

### Start Scraping Jobs
1. Go to Dashboard
2. Click "Start New Scrape" button (top right)
3. Enter job title (e.g., "Data Scientist")
4. Enter location (e.g., "Germany")
5. Click "Start Scraping"
6. Wait for status alert
7. Refresh page to see new jobs

### Apply Filters
1. On Dashboard, click "Filters" button
2. Select from dropdowns:
   - Source (LinkedIn, Indeed, etc.)
   - Job Type (Full-time, Contract, etc.)
   - Location Type (Remote, Hybrid, On-site)
   - Experience Level
   - Date Posted
3. Or use quick match score buttons (60%, 70%, 80%+)

### Prepare for Interview
1. Go to Applications page
2. Find the application
3. Change status to "Interview"
4. Set interview date (optional)
5. Go to Interview Prep page
6. Select the job from left sidebar
7. Review and prepare for each question
8. Add notes for each
9. Mark questions as prepared

### Export Analytics
1. Go to Analytics page
2. Option 1: Click "CSV" on any chart
3. Option 2: Click "Export All Data" (top right)
4. File downloads automatically with date

---

## 🛠️ Troubleshooting

### Docker Build Error (snapshot does not exist)
**Solution**: Use the build script which uses `--no-cache`
```bash
./build.sh
```

### Frontend Not Loading
```bash
sudo docker compose logs frontend
```
Check for errors, then:
```bash
sudo docker compose restart frontend
```

### Backend API Not Responding
```bash
sudo docker compose logs backend
```
Check for errors, then:
```bash
sudo docker compose restart backend
```

### Database Issues
```bash
# Reset database (WARNING: Deletes all data)
sudo docker compose down -v
./start.sh
```

### Port Already in Use
```bash
# Find what's using port 3000 or 8000
sudo lsof -i :3000
sudo lsof -i :8000

# Kill the process
sudo kill -9 <PID>
```

---

## 📊 View Logs

### All services
```bash
sudo docker compose logs -f
```

### Specific service
```bash
sudo docker compose logs -f frontend
sudo docker compose logs -f backend
```

### Last 50 lines
```bash
sudo docker compose logs --tail=50
```

---

## 🛑 Stop the Application

```bash
./stop.sh
```

Or manually:
```bash
sudo docker compose down
```

---

## 🎨 What's New in This Version

✅ **Dashboard**: Modern gradient design, advanced filters, scrape controls
✅ **ATS Score**: Detailed breakdown with keyword match, formatting, missing elements
✅ **Interview Prep**: Auto-categorized questions with notes and progress tracking
✅ **Analytics**: Enhanced charts, CSV export, skills demand, success metrics
✅ **Responsive**: Full-width layout, mobile-friendly
✅ **Modern UI**: Gradients, animations, smooth transitions

---

## 📞 Need Help?

1. Check `IMPLEMENTATION_COMPLETE.md` for detailed feature documentation
2. Check Docker logs for errors
3. Verify all containers are running: `sudo docker compose ps`
4. Try rebuilding: `./build.sh`

---

**🎉 Enjoy your fully automated job hunting platform!**
