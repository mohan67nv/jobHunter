# 🔑 API Keys Setup Guide

## Where to Get Your API Keys

### 1. Google Gemini Pro API Key (Required)

**Get it here**: https://makersuite.google.com/app/apikey

**Steps**:
1. Go to https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Click "Create API key in new project" (or use existing)
5. Copy the generated API key (starts with `AIza...`)

**Note**: Gemini Pro is FREE with generous limits:
- 60 requests per minute
- 1500 requests per day
- Perfect for job hunting!

---

### 2. GitHub API Key (Optional)

**Note**: There's no "GitHub Pro" API for this project. You might be thinking of:

**Option A: Anthropic Claude API** (Optional alternative AI)
- Get it here: https://console.anthropic.com/
- Sign up and navigate to API Keys
- Generate a new key

**Option B: OpenAI GPT-4 API** (Optional alternative AI)
- Get it here: https://platform.openai.com/api-keys
- Sign up and create API key
- Note: This costs money (pay-per-use)

---

## Where to Paste Your API Keys

### Method 1: Environment File (Recommended)

**Edit the `.env` file in the project root:**

```bash
# Open the .env file
nano .env

# Or use any text editor
code .env
# or
vim .env
```

**Add your keys**:
```bash
# Required - Gemini Pro API Key
GEMINI_API_KEY=AIzaSyDxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Optional - Alternative AI providers
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Other settings (keep defaults for now)
DATABASE_URL=sqlite:///data/jobhunter.db
ENVIRONMENT=development
DEBUG=True
SCRAPE_INTERVAL_HOURS=2
ANALYSIS_INTERVAL_HOURS=4
```

**Save the file** (Ctrl+X, then Y, then Enter if using nano)

---

### Method 2: Direct Environment Variables (Temporary)

```bash
# Set for current session only
export GEMINI_API_KEY="AIzaSyDxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
export ANTHROPIC_API_KEY="sk-ant-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
export OPENAI_API_KEY="sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

---

### Method 3: Through Docker (if using Docker)

The `.env` file is automatically read by docker-compose, so just edit `.env` as shown in Method 1.

---

## Testing Your API Keys

### Test Gemini API Key

```bash
# Activate virtual environment
cd backend
source jobHunter/bin/activate

# Test the key
python -c "
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv('../.env')
api_key = os.getenv('GEMINI_API_KEY')

if not api_key:
    print('❌ GEMINI_API_KEY not found in .env file!')
else:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content('Say hello!')
        print('✅ Gemini API Key is working!')
        print(f'Response: {response.text}')
    except Exception as e:
        print(f'❌ Error: {e}')
"
```

---

## Current Status of Your Setup

✅ **Python Environment**: Created (`jobHunter` virtual environment)
✅ **Packages**: Installed (all requirements.txt packages)
✅ **Database**: SQLite database created with all tables
✅ **Project Structure**: Complete

⚠️ **API Key**: You need to add your Gemini API key to `.env` file

---

## Quick Setup Checklist

- [ ] Get Gemini API key from https://makersuite.google.com/app/apikey
- [ ] Copy the API key
- [ ] Open `.env` file in project root
- [ ] Paste: `GEMINI_API_KEY=your_actual_key_here`
- [ ] Save the file
- [ ] Test with the command above

---

## Security Notes

⚠️ **IMPORTANT**:
- Never commit `.env` file to Git (already in .gitignore)
- Keep your API keys secret
- Don't share your `.env` file
- Regenerate keys if accidentally exposed

---

## Need Help?

If you have issues:
1. Make sure the `.env` file is in the project root (not in backend/ folder)
2. Check that there are no extra spaces around the `=` sign
3. Make sure the key starts with the correct prefix:
   - Gemini: `AIza...`
   - Anthropic: `sk-ant-...`
   - OpenAI: `sk-proj-...`

---

**Next Step**: After adding your API key, you can start the application!

```bash
# Option 1: Using Docker (recommended)
docker-compose up

# Option 2: Without Docker
# Terminal 1 - Backend
cd backend
source jobHunter/bin/activate
uvicorn app:app --reload

# Terminal 2 - Frontend
cd frontend
npm install
npm run dev
```
