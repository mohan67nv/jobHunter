# Quick Testing Guide - Multi-Layer ATS

## 🚀 How to Test

### Prerequisites
- Backend running: `docker ps` (check jobhunter_backend)
- Frontend running: `docker ps` (check jobhunter_frontend)
- API healthy: `curl http://localhost:8000/health`

---

## 📋 Test Scenarios

### Test 1: Basic Tier (Score Only)
```bash
curl -X POST 'http://localhost:8000/api/analysis/enhanced-ats-scan/1?use_multi_layer=true&tier=basic' \
  -H 'Content-Type: application/json' | jq
```

**Expected Output:**
- final_score (0-100)
- confidence (0.0-1.0)
- layer_scores (Layer 1 + Layer 2)
- No detailed feedback

---

### Test 2: Standard Tier (Score + Insights)
```bash
curl -X POST 'http://localhost:8000/api/analysis/enhanced-ats-scan/1?use_multi_layer=true&tier=standard' \
  -H 'Content-Type: application/json' | jq
```

**Expected Output:**
- All Basic tier data
- Layer 3 processed (feedback_generated: true)
- Standard-level insights
- Upgrade prompt for premium

---

### Test 3: Premium Tier (Full Feedback)
```bash
curl -X POST 'http://localhost:8000/api/analysis/enhanced-ats-scan/1?use_multi_layer=true&tier=premium' \
  -H 'Content-Type: application/json' | jq
```

**Expected Output:**
- All Standard tier data
- detailed_feedback object with:
  - immediate_fixes (3 quick wins)
  - strategic_improvements
  - keyword_placement
  - star_stories
  - formatting_tips
- cost_breakdown for all 3 layers

---

### Test 4: Legacy Mode (Backward Compatibility)
```bash
curl -X POST 'http://localhost:8000/api/analysis/enhanced-ats-scan/1' \
  -H 'Content-Type: application/json' | jq
```

**Expected Output:**
- Traditional 30+ checks format
- keyword_analysis
- font_check
- layout_check
- page_setup_check
- structure_analysis

---

## 🔍 What to Verify

### ✅ Functionality Checks
- [ ] All 3 tiers return different amounts of data
- [ ] Layer 1 + Layer 2 always run (all tiers)
- [ ] Layer 3 only includes full feedback for premium
- [ ] Scores are consistent (within reason)
- [ ] Confidence score makes sense (higher for closer Layer 1/2 agreement)
- [ ] Cost tracking works (increases: basic < standard < premium)

### ✅ Performance Checks
- [ ] Basic tier: < 10 seconds
- [ ] Standard tier: < 15 seconds
- [ ] Premium tier: < 20 seconds
- [ ] No errors in docker logs
- [ ] API remains responsive

### ✅ Quality Checks
- [ ] Scores make sense for given resume/JD
- [ ] Feedback is actionable (premium tier)
- [ ] Keyword matching is accurate
- [ ] Refinements from Layer 2 are logical

---

## 🐛 Troubleshooting

### Issue: 404 Job Not Found
**Solution:** Create a job first or use existing job_id
```bash
# Check available jobs
curl http://localhost:8000/api/jobs | jq
```

### Issue: 400 No Resume Found
**Solution:** Upload resume in user profile
```bash
# Check user profile
curl http://localhost:8000/api/user/profile | jq
```

### Issue: Slow Response
**Reason:** AI models take 10-20 seconds to process
**Expected:** Wait patiently for all 3 layers to complete

### Issue: API Key Error
**Solution:** Verify environment variables
```bash
docker exec jobhunter_backend env | grep -E "(DEEPSEEK|OPENAI)_API_KEY"
```

---

## 📊 Sample Test Output

### Basic Tier Response
```json
{
  "job_id": 1,
  "scoring_mode": "multi_layer",
  "tier": "basic",
  "final_score": 85,
  "confidence": 0.92,
  "layer_scores": [
    {"layer": 1, "model": "DeepSeek-Chat-V3", "score": 82},
    {"layer": 2, "model": "GPT-5-mini", "score": 88}
  ],
  "processing_time": 8.2
}
```

### Premium Tier Response
```json
{
  "job_id": 1,
  "scoring_mode": "multi_layer",
  "tier": "premium",
  "final_score": 85,
  "confidence": 0.92,
  "layer_scores": [...],
  "detailed_feedback": {
    "immediate_fixes": [
      {
        "action": "Add 'Python' to skills section",
        "impact": "High",
        "reasoning": "Required skill missing"
      }
    ],
    "strategic_improvements": [...],
    "keyword_placement": [...],
    "star_stories": [...],
    "formatting_tips": [...]
  },
  "cost_breakdown": {
    "layer1": 0.0001,
    "layer2": 0.0002,
    "layer3": 0.0003,
    "total": 0.0006
  },
  "processing_time": 15.7
}
```

---

## 🎯 Testing Checklist

Before pushing to Git:
- [ ] Test all 3 tiers (basic, standard, premium)
- [ ] Test legacy mode (use_multi_layer=false)
- [ ] Verify scores are reasonable (40-95 range)
- [ ] Check feedback quality (premium tier)
- [ ] Confirm cost tracking works
- [ ] Check docker logs for errors
- [ ] Test with different resumes/JDs
- [ ] Verify confidence calculation
- [ ] Check processing times
- [ ] API docs updated

---

## 🔧 Quick Commands

```bash
# Restart backend to pick up code changes
docker restart jobhunter_backend && sleep 5

# Check backend logs
docker logs jobhunter_backend --tail 50

# Test API health
curl http://localhost:8000/health

# Run validation script
docker exec jobhunter_backend python validate_multi_layer.py

# Check running containers
docker ps

# Access API documentation
open http://localhost:8000/docs  # or visit in browser
```

---

**Ready to Test!** 🚀

Start with Basic tier, then Standard, then Premium to see the progression.
