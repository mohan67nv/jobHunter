# Technical Q&A Enhancement - Glassdoor + CV-Based Questions

## What Changed

### Enhanced Technical Q&A Section
The technical interview questions now include **THREE types of questions** (15-20 total):

#### 1. 🔍 Glassdoor & Real Candidate Questions (5-7 questions)
- **Real interview questions** reported by actual candidates at the company
- Sourced from Glassdoor, Blind, LeetCode Discuss
- Company-specific interview patterns
- Coding platform questions (LeetCode, HackerRank)

**Badge:** 🔍 Glassdoor | 👤 Real Interview

#### 2. 📋 Job-Specific Technical Questions (5-7 questions)
- Based on the job description requirements
- Role-specific technical depth
- Technology stack mentioned in JD

**Badge:** 📋 Job-Specific

#### 3. 🎯 Your Project/Experience Questions (5-7 questions)
- **Personalized questions about YOUR specific projects from your resume**
- "Tell me about your [project name]" deep-dives
- Technical architecture questions about your work
- Challenges and decisions you made
- **"How to Explain This" guidance** for each project question
- Suggested metrics and results to highlight

**Badge:** 🎯 Your Project | 📁 [Project Name]

## New Features

### Backend Enhancements

#### 1. Resume Integration
**File:** `backend/ai_agents/researcher.py`

```python
def process(company_name, job_title, job_description, resume_text):
    # Now accepts resume_text parameter
    technical_qa = self._generate_technical_qa(..., resume_text)
```

#### 2. Enhanced Technical Q&A Generation
- Prompts now request 3 distinct question types
- Increased max_tokens to 6000 (from 4000) for more comprehensive responses
- Added fields: `source`, `project_context`, `explanation_approach`

#### 3. User Resume Fetching
**File:** `backend/routers/analysis.py`

```python
# Get user's resume for personalized project questions
user = db.query(UserProfile).filter(UserProfile.id == 1).first()
resume_text = user.resume_text if user else None

researcher.process(..., resume_text=resume_text)
```

### Frontend Enhancements

#### 1. Source Badges
**New badges to identify question types:**
- 🔍 Glassdoor (emerald)
- 👤 Real Interview (teal)
- 🎯 Your Project (purple)
- 📋 Job-Specific (blue)

#### 2. Project Context Display
- Shows which project the question relates to
- Displays as: 📁 [Project Name]

#### 3. Explanation Guidance
**New purple callout box:**
```
💡 How to Explain This:
[Specific guidance on how to present this project/experience]
```

#### 4. Enhanced Pro Tip
Updated tip section to inform users about the three question types.

## Question Structure

### Enhanced JSON Schema

```json
{
  "question": "Tell me about your [specific project] and the architecture decisions you made",
  "answer": "Comprehensive answer with technical details...",
  "difficulty": "Medium",
  "category": "Project-Experience",
  "source": "candidate_project",
  "project_context": "ML Pipeline System",
  "explanation_approach": "Start with business problem, then technical solution, highlight scalability decisions, mention results with metrics",
  "key_points": [
    "Explain business context first",
    "Detail technical architecture",
    "Highlight scalability decisions",
    "Mention measurable results"
  ],
  "follow_ups": [
    "What would you do differently now?",
    "How did you handle [specific challenge]?"
  ]
}
```

## Visual Changes

### Before
```
[Medium] [System Design]
Question: How would you design a scalable system?
```

### After
```
[Medium] [System Design] [🔍 Glassdoor] [📁 ML Pipeline System]
Question: Tell me about your ML Pipeline project - how did you ensure scalability?

💡 How to Explain This:
Start with the business problem you were solving, then describe the 
architecture, emphasize your specific contributions, and end with 
measurable results (e.g., "reduced processing time by 40%").

Answer:
[Detailed answer...]

Key Points:
✓ Explain business context
✓ Detail technical decisions
✓ Highlight your role
✓ Share metrics

Possible Follow-ups:
• What challenges did you face?
• How would you improve it now?
```

## Example Questions Generated

### From Glassdoor
**Source: Real candidate reports**
```
Q: BMW asks a lot about C++ optimization for embedded systems. 
   Can you explain cache optimization techniques?
   
Badge: [Hard] [Performance] [🔍 Glassdoor]
```

### From Job Description
**Source: JD requirements**
```
Q: The role requires experience with TensorFlow and PyTorch. 
   How do you decide which framework to use for a project?
   
Badge: [Medium] [ML] [📋 Job-Specific]
```

### From Your Resume
**Source: Your CV projects**
```
Q: Tell me about your "Real-time Fraud Detection System" project. 
   How did you handle the latency requirements?
   
Badge: [Medium] [Project-Experience] [🎯 Your Project] [📁 Fraud Detection]

💡 How to Explain This:
Start by explaining the business impact (e.g., "Detected fraud in <100ms 
saving $2M annually"), then dive into the technical approach (streaming 
pipeline, model optimization), and end with challenges overcome.
```

## How It Works

### AI Prompt Strategy

The enhanced prompt instructs the AI to:

1. **Search Knowledge Base** for actual interview questions at the company
   - "Search your knowledge for actual interview questions asked at [Company]"
   - "Include questions from Glassdoor, Blind, LeetCode Discuss"

2. **Analyze Job Description** for role-specific questions
   - Extract required technologies and skills
   - Generate questions matching complexity level

3. **Parse Resume** for project-specific questions
   - Identify projects, technologies used, and achievements
   - Generate "Tell me about..." questions for each major project
   - Provide guidance on how to explain effectively

### Resume Parsing
- System extracts up to 3000 characters from resume
- AI identifies project names, technologies, and responsibilities
- Generates contextualized questions about YOUR work
- Provides tailored explanation strategies

## Benefits

### For You
✅ **Glassdoor Insights** - Know what real candidates were asked  
✅ **Project Preparation** - Practice explaining YOUR specific work  
✅ **Explanation Guidance** - Learn best way to present your projects  
✅ **Role Alignment** - Questions match job requirements exactly  
✅ **Confidence Building** - Prepared for questions about your experience  

### Technical
- Increased from 10-15 questions to 15-20 questions
- More personalized and relevant questions
- Better interview readiness
- Covers all question types you'll face

## Testing

### With Resume
1. Ensure your resume is uploaded in Profile section
2. Create application with status="interview"
3. Go to Interview Prep → Technical tab
4. Look for badges: 🔍 🎯 📋
5. Expand project questions to see "How to Explain This" guidance

### Without Resume
- System gracefully handles missing resume
- Generates Glassdoor + Job-specific questions only
- Still provides 10-15 quality technical questions

## Configuration

### Adjusting Question Distribution
Edit in `researcher.py`:
```python
# Change numbers in prompt:
# 1. GLASSDOOR/REAL CANDIDATE QUESTIONS (5-7 questions)  ← Modify here
# 2. JOB-SPECIFIC TECHNICAL QUESTIONS (5-7 questions)    ← Modify here
# 3. CANDIDATE'S PROJECT/EXPERIENCE QUESTIONS (5-7 questions) ← Modify here
```

### Resume Character Limit
Default: 3000 characters
```python
resume_context = f"\n\nCandidate's Resume/CV:\n{resume_text[:3000]}"
#                                                           ^^^^ Change here
```

## Files Changed

1. ✅ `backend/ai_agents/researcher.py` - Enhanced Q&A generation
2. ✅ `backend/routers/analysis.py` - Resume fetching and passing
3. ✅ `frontend/src/pages/InterviewPrep.tsx` - Source badges and UI enhancements

## Future Enhancements

- [ ] Parse resume for specific skills and technologies
- [ ] Generate questions for each skill mentioned
- [ ] LinkedIn integration for profile analysis
- [ ] GitHub profile analysis for code review questions
- [ ] Practice mode: Record answers and get AI feedback
- [ ] Compare your answers to best practices

---

**Status:** ✅ Ready to Use  
**Last Updated:** December 31, 2024  
**Version:** 2.0.0
