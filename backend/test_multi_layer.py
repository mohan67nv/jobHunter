"""
Test script for Multi-Layer ATS Scoring System
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from ai_agents.multi_layer_ats import MultiLayerATSScorer

# Sample resume
resume = """
John Doe
Senior Python Developer

SKILLS:
- Python, FastAPI, Django, Flask
- Docker, Kubernetes, AWS
- PostgreSQL, MongoDB, Redis
- React, TypeScript, Node.js
- CI/CD, Git, Linux

EXPERIENCE:
Senior Backend Developer | Tech Corp | 2020-2024
- Built microservices using Python and FastAPI
- Deployed containerized applications with Docker and Kubernetes
- Managed AWS infrastructure (EC2, S3, RDS)
- Improved API response time by 40%
- Led team of 5 developers

Backend Developer | StartupCo | 2018-2020
- Developed REST APIs using Django
- Implemented automated testing with pytest
- Set up CI/CD pipelines with GitHub Actions
- Reduced deployment time by 60%

EDUCATION:
Bachelor of Science in Computer Science
University of Technology, 2018
"""

# Sample job description
job_description = """
Senior Backend Engineer

We're seeking an experienced Backend Engineer to join our team.

REQUIREMENTS:
- 5+ years Python development experience
- Strong experience with FastAPI or Django
- Docker and Kubernetes expertise
- AWS cloud experience (EC2, S3, RDS)
- RESTful API design
- PostgreSQL or MySQL
- CI/CD pipeline experience
- Git version control
- Bachelor's degree in CS or related field

NICE TO HAVE:
- React or frontend experience
- MongoDB or NoSQL databases
- Terraform or infrastructure as code
- Team leadership experience

We offer competitive salary, remote work, and great benefits.
"""


def test_multi_layer_scoring():
    """Test all 3 tiers"""
    print("=" * 80)
    print("🧪 TESTING MULTI-LAYER ATS SCORING SYSTEM")
    print("=" * 80)
    
    scorer = MultiLayerATSScorer()
    
    # Test 1: Basic tier (score only)
    print("\n\n📊 TEST 1: BASIC TIER (Score Only)")
    print("-" * 80)
    result_basic = scorer.assess_resume(resume, job_description, tier='basic')
    print(f"✅ Final Score: {result_basic['final_score']}/100")
    print(f"   Confidence: {result_basic['confidence']:.2f}")
    print(f"   Processing Time: {result_basic['processing_time']:.2f}s")
    print(f"\n   Layer 1 (DeepSeek Chat): {result_basic['layer_scores'][0]['score']}/100")
    print(f"   Layer 2 (GPT-5-mini): {result_basic['layer_scores'][1]['score']}/100")
    print(f"   Keywords Matched: {result_basic['layer_scores'][0].get('keywords_matched', 'N/A')}")
    
    # Test 2: Standard tier (score + insights)
    print("\n\n📊 TEST 2: STANDARD TIER (Score + Insights)")
    print("-" * 80)
    result_standard = scorer.assess_resume(resume, job_description, tier='standard')
    print(f"✅ Final Score: {result_standard['final_score']}/100")
    print(f"   Confidence: {result_standard['confidence']:.2f}")
    print(f"   Processing Time: {result_standard['processing_time']:.2f}s")
    print(f"\n   All 3 layers processed:")
    for layer in result_standard['layer_scores']:
        print(f"   - Layer {layer['layer']} ({layer['model']}): {layer.get('score', 'feedback')}")
    
    # Test 3: Premium tier (full feedback)
    print("\n\n📊 TEST 3: PREMIUM TIER (Full Feedback)")
    print("-" * 80)
    result_premium = scorer.assess_resume(resume, job_description, tier='premium')
    print(f"✅ Final Score: {result_premium['final_score']}/100")
    print(f"   Confidence: {result_premium['confidence']:.2f}")
    print(f"   Processing Time: {result_premium['processing_time']:.2f}s")
    
    if result_premium.get('detailed_feedback'):
        feedback = result_premium['detailed_feedback']
        print(f"\n   📝 Detailed Feedback Available:")
        if feedback.get('immediate_fixes'):
            print(f"      - {len(feedback['immediate_fixes'])} immediate fixes")
        if feedback.get('strategic_improvements'):
            print(f"      - {len(feedback['strategic_improvements'])} strategic improvements")
    
    # Cost breakdown
    print("\n\n💰 COST BREAKDOWN")
    print("-" * 80)
    print(f"   Layer 1 (DeepSeek Chat): ${result_premium['cost_breakdown']['layer1']:.4f}")
    print(f"   Layer 2 (GPT-5-mini): ${result_premium['cost_breakdown']['layer2']:.4f}")
    print(f"   Layer 3 (DeepSeek Reasoner): ${result_premium['cost_breakdown']['layer3']:.4f}")
    print(f"   Total: ${result_premium['cost_breakdown']['total']:.4f}")
    
    print("\n" + "=" * 80)
    print("✅ ALL TESTS COMPLETED SUCCESSFULLY")
    print("=" * 80)


if __name__ == "__main__":
    try:
        test_multi_layer_scoring()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
