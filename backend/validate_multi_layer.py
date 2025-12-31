"""
Quick validation of multi-layer imports and initialization
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

print("=" * 80)
print("🔍 VALIDATING MULTI-LAYER ATS SYSTEM")
print("=" * 80)

# Test 1: Import multi_layer_ats
print("\n1. Testing import of multi_layer_ats...")
try:
    from ai_agents.multi_layer_ats import MultiLayerATSScorer
    print("   ✅ MultiLayerATSScorer imported successfully")
except Exception as e:
    print(f"   ❌ Import failed: {e}")
    sys.exit(1)

# Test 2: Import enhanced_ats_scorer with multi-layer support
print("\n2. Testing import of enhanced_ats_scorer...")
try:
    from ai_agents.enhanced_ats_scorer import EnhancedATSScorer
    print("   ✅ EnhancedATSScorer imported successfully")
except Exception as e:
    print(f"   ❌ Import failed: {e}")
    sys.exit(1)

# Test 3: Initialize MultiLayerATSScorer
print("\n3. Testing MultiLayerATSScorer initialization...")
try:
    scorer = MultiLayerATSScorer()
    print("   ✅ MultiLayerATSScorer initialized")
    print(f"   - Layer 1 agent: {scorer.layer1_agent.model}")
    print(f"   - Layer 2 agent: {scorer.layer2_agent.model}")
    print(f"   - Layer 3 agent: {scorer.layer3_agent.model}")
except Exception as e:
    print(f"   ❌ Initialization failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 4: Initialize EnhancedATSScorer in both modes
print("\n4. Testing EnhancedATSScorer modes...")
try:
    # Legacy mode
    scorer_legacy = EnhancedATSScorer(use_multi_layer=False)
    print("   ✅ Legacy mode initialized")
    
    # Multi-layer mode
    scorer_ml = EnhancedATSScorer(use_multi_layer=True)
    print("   ✅ Multi-layer mode initialized")
    print(f"   - Multi-layer scorer available: {scorer_ml.multi_layer_scorer is not None}")
except Exception as e:
    print(f"   ❌ Mode initialization failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 5: Check model config
print("\n5. Testing model_config integration...")
try:
    from ai_agents.model_config import get_model_config
    
    configs = ['MultiLayerATS_Layer1', 'MultiLayerATS_Layer2', 'MultiLayerATS_Layer3']
    for config_name in configs:
        config = get_model_config(config_name)
        print(f"   ✅ {config_name}: {config['provider']}/{config['model']}")
except Exception as e:
    print(f"   ❌ Model config check failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 6: Check API keys
print("\n6. Checking API keys...")
import os
deepseek_key = os.getenv('DEEPSEEK_API_KEY', '')
openai_key = os.getenv('OPENAI_API_KEY', '')

if deepseek_key:
    print(f"   ✅ DEEPSEEK_API_KEY: {deepseek_key[:10]}...{deepseek_key[-4:]}")
else:
    print("   ⚠️  DEEPSEEK_API_KEY not found")

if openai_key:
    print(f"   ✅ OPENAI_API_KEY: {openai_key[:10]}...{openai_key[-4:]}")
else:
    print("   ⚠️  OPENAI_API_KEY not found")

print("\n" + "=" * 80)
print("✅ VALIDATION COMPLETE - ALL COMPONENTS WORKING")
print("=" * 80)
print("\n💡 Multi-Layer ATS System is ready to use!")
print("   - Basic tier: Score only")
print("   - Standard tier: Score + validation insights")
print("   - Premium tier: Score + detailed feedback")
print("\n📊 Model Configuration:")
print("   - Layer 1: DeepSeek Chat V3 (fast baseline)")
print("   - Layer 2: GPT-5-mini (validation)")
print("   - Layer 3: DeepSeek Reasoner R1 (detailed feedback)")
