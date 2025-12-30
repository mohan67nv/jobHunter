# 🚀 QuickStart Guide - SmartJobHunter Pro

Get up and running in 5 minutes!

## Step 1: Prerequisites

Make sure you have:
- ✅ Python 3.11+
- ✅ Node.js 18+
- ✅ Docker & Docker Compose
- ✅ A Google Gemini API key (free at https://makersuite.google.com/app/apikey)

## Step 2: Setup

```bash
# Clone or extract the project
cd smartjobhunter

# Run the setup script
chmod +x scripts/setup.sh
./scripts/setup.sh
```

## Step 3: Configure

Edit the `.env` file and add your API key:
```bash
GEMINI_API_KEY=your_actual_api_key_here
```

## Step 4: Start

```bash
# Start all services
docker-compose up
```

Wait for the services to start (30-60 seconds).

## Step 5: Use

1. **Open the dashboard**: http://localhost:3000
2. **Go to Settings** (top right)
3. **Upload your resume** (Profile tab)
4. **Set your preferences** (Preferences tab - keywords, locations)
5. **Go back to Dashboard**
6. **Click "Start Scraping"** or use the search bar

That's it! The system will:
- Scrape jobs from multiple sources
- Automatically analyze them with AI
- Show you match scores and recommendations
- Track your applications

## Quick Commands

```bash
# Start the application
docker-compose up

# Start in background
docker-compose up -d

# Stop the application
docker-compose down

# View logs
docker-compose logs -f

# Rebuild after changes
docker-compose build
docker-compose up
```

## Test the API

Visit http://localhost:8000/docs for interactive API documentation.

## Troubleshooting

**Problem**: Port already in use
```bash
# Stop any existing services
docker-compose down
# Or change ports in docker-compose.yml
```

**Problem**: Database errors
```bash
# Reset database
rm data/jobhunter.db
docker-compose run --rm backend python -c "from database import init_db; init_db()"
```

**Problem**: Frontend won't start
```bash
cd frontend
npm install
npm run dev
```

## Next Steps

1. **Customize scraping**: Edit `backend/config.py` to adjust scraping intervals
2. **Add more companies**: Edit `scripts/seed_companies.py`
3. **Schedule automation**: The app auto-scrapes every 2 hours by default
4. **Export data**: Use the Analytics page to download reports

## Getting Help

- Check the full README.md for detailed documentation
- Visit http://localhost:8000/docs for API documentation
- Check logs: `docker-compose logs backend` or `docker-compose logs frontend`

Happy job hunting! 🎯
