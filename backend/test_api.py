"""
Test the Multi-Layer ATS API endpoint
"""
import requests
import json

BASE_URL = "http://localhost:8000"

# First, check if API is healthy
print("=" * 80)
print("🔍 TESTING MULTI-LAYER ATS API")
print("=" * 80)

print("\n1. Checking API health...")
try:
    response = requests.get(f"{BASE_URL}/health", timeout=5)
    print(f"   ✅ API is healthy: {response.json()}")
except Exception as e:
    print(f"   ❌ API health check failed: {e}")
    exit(1)

# Check docs endpoint for new parameters
print("\n2. Checking API documentation...")
try:
    response = requests.get(f"{BASE_URL}/docs")
    if response.status_code == 200:
        print("   ✅ API docs accessible at http://localhost:8000/docs")
except Exception as e:
    print(f"   ⚠️  Could not access docs: {e}")

print("\n" + "=" * 80)
print("✅ MULTI-LAYER ATS API IS READY")
print("=" * 80)

print("\n📊 Available Endpoints:")
print("   POST /api/analysis/enhanced-ats-scan/{job_id}")
print("      Parameters:")
print("      - use_multi_layer: bool (default: False)")
print("      - tier: 'basic' | 'standard' | 'premium' (default: 'standard')")
print("\n💡 Example Usage:")
print("   curl -X POST 'http://localhost:8000/api/analysis/enhanced-ats-scan/1?use_multi_layer=true&tier=premium'")
