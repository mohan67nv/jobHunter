# Interview Preparation Feature - Complete Documentation

## Overview
Comprehensive AI-powered interview preparation system with three specialized sections: Company Information, Technical Q&A, Behavioral Q&A, and HR Q&A. Uses Perplexity AI for real-time company research and contextual question generation.

## Features

### 1. Company Information Section
**What it provides:**
- **Company Overview**
  - Industry, size, headquarters, founded date
  - Company description and mission statement
  - Main products and services
  
- **Recent News & Developments** (Last 6 months)
  - News headlines with dates
  - Brief summaries
  - Interview relevance (why it matters for your interview)
  
- **Company Culture**
  - Core values
  - Work environment description
  - Work-life balance insights
  - Diversity & inclusion initiatives
  - Employee reviews summary
  
- **Company-Specific Q&A** (5-10 questions)
  - Question: "Why do you want to work at [Company]?"
  - Personalized Answer: 3-4 sentences with specific references
  - Key Talking Points: Bullet list of important points
  - Reference: Specific news/products to mention
  
- **Smart Questions to Ask**
  - Thoughtful questions to ask the interviewer
  - Explanation of why each question is strategic

### 2. Technical Q&A Section (10-15 questions)
**What it provides:**
- **Difficulty-rated questions** (Easy/Medium/Hard)
- **Category tags** (System Design, Algorithms, ML, Cloud, Database, etc.)
- **Comprehensive answers** (4-6 sentences minimum)
- **Key points** breakdown
- **Follow-up questions** to expect

**Example question types:**
- System design questions for senior roles
- Coding/algorithm questions for engineering roles
- ML/AI questions for data science roles
- Cloud architecture for cloud roles
- Database design for backend roles
- Performance optimization
- Security best practices
- Testing strategies

### 3. Behavioral Q&A Section (10-12 questions)
**What it provides:**
- **STAR Method structured answers**
  - 📍 Situation: Context and background
  - 🎯 Task: What needed to be accomplished
  - ⚡ Action: Specific actions taken
  - 🏆 Result: Outcome with metrics
  
- **Competency tags** (Leadership, Teamwork, Problem-Solving, Communication, etc.)
- **Complete answer** in narrative form
- **Tips** for answering effectively

**Topics covered:**
- Leadership and team management
- Handling conflict and difficult situations
- Problem-solving and decision-making
- Adaptability and change management
- Communication and collaboration
- Taking initiative and ownership
- Handling failure and learning
- Time management and prioritization

### 4. HR Round Section (8-10 questions)
**What it provides:**
- **Strategic answers** positioned for success
- **Example answers** tailored to the role
- **Do's and Don'ts** side-by-side
- **Category tags** (Career Goals, Strengths-Weaknesses, Motivation, Salary, etc.)

**Topics covered:**
- Career goals and motivation
- Strengths and weaknesses
- Salary expectations
- Work style and preferences
- Why leaving current role
- Handling work pressure
- Availability and notice period
- Long-term career plans

## How It Works

### Backend (Python/FastAPI)

#### 1. Enhanced CompanyResearcher Agent
**File:** `backend/ai_agents/researcher.py`

**Main method:**
```python
def process(company_name, job_title, job_description) -> Dict:
    return {
        "company_info": self._generate_company_info(...),
        "technical_qa": self._generate_technical_qa(...),
        "behavioral_qa": self._generate_behavioral_qa(...),
        "hr_qa": self._generate_hr_qa(...)
    }
```

**Key features:**
- Uses Perplexity AI provider for real-time research
- Generates structured JSON responses
- Fallback methods for graceful degradation
- Comprehensive prompts with explicit JSON schemas

#### 2. Updated API Endpoint
**File:** `backend/routers/analysis.py`

**Endpoint:** `GET /api/analysis/interview-prep/{job_id}`

**Response structure:**
```json
{
  "job_id": 123,
  "job_title": "Senior ML Engineer",
  "company": "TechCorp",
  "company_info": {
    "overview": {...},
    "recent_news": [...],
    "culture": {...},
    "company_qa": [...],
    "questions_to_ask": [...]
  },
  "technical_qa": [
    {
      "question": "...",
      "answer": "...",
      "difficulty": "Medium",
      "category": "ML",
      "key_points": [...],
      "follow_ups": [...]
    }
  ],
  "behavioral_qa": [...],
  "hr_qa": [...]
}
```

### Frontend (React/TypeScript)

#### 1. Interview Prep Page
**File:** `frontend/src/pages/InterviewPrep.tsx`

**Features:**
- Four-tab interface (Company, Technical, Behavioral, HR)
- Expandable Q&A cards with show/hide functionality
- Difficulty badges for technical questions
- Competency tags for behavioral questions
- STAR method breakdown display
- Do's and Don'ts side-by-side for HR questions
- Color-coded sections for easy navigation

**UI Components:**
- Job selection sidebar (shows all interviews)
- Job header with gradient background
- Tab navigation with question counts
- Expandable cards with chevron icons
- Color-coded badges and tags
- Loading states with spinner
- Empty state for no interviews

## How to Use

### For Users

1. **Set Application Status to "Interview"**
   - Go to Applications page
   - Find the job you're interviewing for
   - Change status to "Interview" from dropdown

2. **Navigate to Interview Prep**
   - Click "Interview Prep" in navigation menu
   - Select the job from the sidebar (if multiple interviews)

3. **Explore Company Information**
   - Read company overview and mission
   - Review recent news and why it matters
   - Study company culture and values
   - Practice company-specific Q&A
   - Prepare smart questions to ask

4. **Practice Technical Questions**
   - Click "Technical" tab
   - Review questions by difficulty
   - Click to expand and see detailed answers
   - Note key points and follow-up questions
   - Practice explaining solutions out loud

5. **Prepare Behavioral Answers**
   - Click "Behavioral" tab
   - Review STAR-method structured answers
   - Adapt examples to your own experience
   - Practice delivering answers concisely
   - Use tips provided for each question

6. **Master HR Questions**
   - Click "HR Round" tab
   - Review strategic answers
   - Study do's and don'ts
   - Prepare honest but strategic responses
   - Practice sounding confident and genuine

### For Developers

#### Adding New Question Types

1. **Update prompt in researcher.py:**
```python
def _generate_technical_qa(self, company_name, job_title, job_description):
    prompt = f"""
    Generate technical interview questions...
    Include:
    - NEW_CATEGORY questions
    ...
    """
```

2. **Update TypeScript interfaces:**
```typescript
interface TechnicalQA {
  question: string
  answer: string
  // Add new fields here
}
```

3. **Update UI rendering:**
```tsx
{qa.new_field && (
  <div>Display new field</div>
)}
```

#### Customizing AI Prompts

Edit prompts in `backend/ai_agents/researcher.py`:
- `_generate_company_info()` - Company research prompt
- `_generate_technical_qa()` - Technical questions prompt
- `_generate_behavioral_qa()` - Behavioral questions prompt
- `_generate_hr_qa()` - HR questions prompt

#### Changing AI Provider

Default is Perplexity for real-time research. To change:
```python
def __init__(self, preferred_provider: str = "perplexity"):
    super().__init__(preferred_provider="openai")  # or "claude", "gemini"
```

## API Response Times

- **Company Info:** ~10-15 seconds (real-time research)
- **Technical Q&A:** ~15-20 seconds (10-15 questions)
- **Behavioral Q&A:** ~15-20 seconds (10-12 questions)
- **HR Q&A:** ~10-15 seconds (8-10 questions)
- **Total:** ~50-70 seconds for complete prep

**Optimization tip:** Generate sections in parallel (future enhancement)

## Error Handling

### Backend
- Graceful fallback to default questions if AI fails
- Catches JSON parsing errors
- Returns fallback data structure
- Logs errors with detailed context

### Frontend
- Loading states during generation
- Empty state if no interviews scheduled
- Error boundary for unexpected crashes
- Retry mechanism (via React Query)

## Testing

### Backend Testing
```bash
cd backend
python -m pytest tests/test_researcher.py -v
```

### Frontend Testing
```bash
cd frontend
npm run test -- InterviewPrep.test.tsx
```

### Manual Testing
1. Create a test job in database
2. Create application with status="interview"
3. Visit `/interview-prep` page
4. Click on test job
5. Verify all tabs load correctly
6. Test expand/collapse functionality
7. Verify all data displays properly

## Performance Considerations

### Backend
- AI generation can take 10-20 seconds per section
- Use background tasks for non-blocking
- Cache results in database (future enhancement)
- Rate limiting on Perplexity API

### Frontend
- React Query caching prevents re-fetching
- Lazy loading of tab content
- Virtual scrolling for large question lists (future)
- Debounced search/filter (future)

## Future Enhancements

### Short-term
- [ ] Save/bookmark specific questions
- [ ] Add personal notes to questions
- [ ] Mark questions as "prepared"
- [ ] Print/export interview prep as PDF
- [ ] Practice mode (hide answers initially)

### Medium-term
- [ ] Video recording for practice answers
- [ ] AI feedback on practice answers
- [ ] Flashcard mode for quick review
- [ ] Share prep materials with team
- [ ] Track preparation progress

### Long-term
- [ ] Mock interview with AI
- [ ] Real-time coaching during practice
- [ ] Interview performance analytics
- [ ] Industry-specific question banks
- [ ] Community-contributed questions

## Troubleshooting

### "No interviews scheduled" message
- Check application status is "interview"
- Verify job_id is valid
- Check database connection

### Loading spinner never stops
- Check backend logs for errors
- Verify Perplexity API key is configured
- Check network requests in browser DevTools
- Verify API endpoint is accessible

### Empty/missing data
- Check API response in Network tab
- Verify JSON parsing is successful
- Check for null/undefined values
- Review backend logs for generation errors

### TypeScript errors
```bash
cd frontend
npm run type-check
```

### Python errors
```bash
cd backend
python -m py_compile ai_agents/researcher.py
```

## Configuration

### Environment Variables
```bash
# Required
PERPLEXITY_API_KEY=your_key_here

# Optional (for fallback providers)
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
GOOGLE_API_KEY=your_key_here
```

### Customization Options

**Number of questions:**
Edit prompts in researcher.py:
```python
prompt = f"""
Generate 10-15 technical questions...  # Change number here
```

**Question difficulty:**
Adjust temperature parameter:
```python
response = self.generate(prompt, temperature=0.5)  # Lower = more consistent
```

**Response length:**
Adjust max_tokens:
```python
response = self.generate(prompt, temperature=0.5, max_tokens=3000)
```

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (React)                          │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  InterviewPrep.tsx                                   │  │
│  │  - Job Selection Sidebar                             │  │
│  │  - Tab Navigation (Company/Tech/Behavioral/HR)       │  │
│  │  - Expandable Q&A Cards                              │  │
│  │  - Color-coded Badges & Tags                         │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ HTTP GET /api/analysis/interview-prep/{job_id}
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   Backend (FastAPI)                          │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  routers/analysis.py                                 │  │
│  │  - GET /interview-prep/{job_id}                      │  │
│  │  - Fetch job from database                           │  │
│  │  - Call CompanyResearcher                            │  │
│  └──────────────────────────────────────────────────────┘  │
│                            │                                 │
│                            ▼                                 │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  ai_agents/researcher.py                             │  │
│  │  - CompanyResearcher.process()                       │  │
│  │  - _generate_company_info()                          │  │
│  │  - _generate_technical_qa()                          │  │
│  │  - _generate_behavioral_qa()                         │  │
│  │  - _generate_hr_qa()                                 │  │
│  └──────────────────────────────────────────────────────┘  │
│                            │                                 │
│                            ▼                                 │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  ai_agents/base_agent.py                             │  │
│  │  - generate() method                                 │  │
│  │  - Provider selection (Perplexity)                   │  │
│  │  - JSON parsing                                      │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ API Call
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                  Perplexity AI API                           │
│  - Real-time company research                                │
│  - Contextual question generation                            │
│  - Structured JSON responses                                 │
└─────────────────────────────────────────────────────────────┘
```

## Code Examples

### Adding Custom Question Category

**Backend:**
```python
def _generate_system_design_qa(self, company_name, job_title, job_description):
    prompt = f"""
    Generate system design interview questions for {job_title} at {company_name}.
    
    Return JSON array:
    [
        {{
            "question": "Design a scalable notification system",
            "answer": "Comprehensive answer...",
            "components": ["API Gateway", "Message Queue", "Workers"],
            "considerations": ["Scalability", "Reliability", "Cost"]
        }}
    ]
    """
    response = self.generate(prompt, temperature=0.5, max_tokens=3000)
    return self.parse_json_response(response) or []
```

**Frontend:**
```typescript
interface SystemDesignQA {
  question: string
  answer: string
  components: string[]
  considerations: string[]
}

// In component
<div>
  <h3>System Design Questions</h3>
  {systemDesignQA.map(qa => (
    <div key={qa.question}>
      <h4>{qa.question}</h4>
      <p>{qa.answer}</p>
      <div>Components: {qa.components.join(', ')}</div>
      <div>Key Considerations: {qa.considerations.join(', ')}</div>
    </div>
  ))}
</div>
```

## Credits

- **AI Provider:** Perplexity Sonar (real-time research)
- **Fallback Providers:** OpenAI GPT-4, Claude, Gemini
- **Framework:** FastAPI (backend), React (frontend)
- **UI Library:** TailwindCSS, Lucide Icons
- **Data Fetching:** TanStack Query (React Query)

## Support

For issues or questions:
1. Check this documentation
2. Review backend logs: `backend/logs/`
3. Check browser console for frontend errors
4. Verify API keys are configured
5. Test API endpoint with curl/Postman

---

**Last Updated:** December 2024  
**Version:** 1.0.0  
**Status:** Production Ready ✅
