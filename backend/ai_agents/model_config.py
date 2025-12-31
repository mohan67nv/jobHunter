"""
Centralized AI Model Configuration
Maps each agent to its optimal model based on task requirements and cost efficiency

Model Strategy:
- deepseek-coder: Code/parsing, structured data extraction (JD parsing, resume optimization)
- deepseek-chat (V3): Fast analysis, matching, baseline scoring
- deepseek-reasoner (R1): Complex reasoning, detailed feedback
- gpt-5-mini (OpenAI): Knowledge tasks, validation, latest data, reliability
"""

# Model routing configuration
# Each agent uses the most cost-effective model for its specific task
MODEL_ROUTING = {
    # Parsing & Code Generation - DeepSeek Coder
    # Fast, accurate for structured data extraction
    "JDAnalyzer": {
        "provider": "deepseek",
        "model": "deepseek-coder"
    },
    
    # Application Optimization - DeepSeek Coder  
    # Best for resume parsing and structured content generation
    "ApplicationOptimizer": {
        "provider": "deepseek",
        "model": "deepseek-coder"
    },
    
    # Matching & Analysis - DeepSeek V3 (Chat)
    # Excellent for reasoning and comparative analysis
    "ResumeMatcher": {
        "provider": "deepseek",
        "model": "deepseek-chat"
    },
    
    # ATS Scoring - Multi-Layer System (uses all 3 models internally)
    # Layer 1: DeepSeek Chat, Layer 2: GPT-5-mini, Layer 3: DeepSeek Reasoner
    "EnhancedATSScorer": {
        "provider": "deepseek",
        "model": "deepseek-chat"  # Base model, multi-layer overrides this
    },
    
    "ATSScorer": {
        "provider": "deepseek",
        "model": "deepseek-chat"
    },
    
    # Company Research - GPT-5-mini
    # Knowledge-heavy task, needs latest data and reliability
    "CompanyResearcher": {
        "provider": "openai",
        "model": "gpt-5-mini"
    },
    
    # Web Scraping - GPT-5-mini
    # Web intelligence and latest scraping patterns
    "AIJobScraper": {
        "provider": "openai",
        "model": "gpt-5-mini"
    },
    
    # Scraper Manager - GPT-5-mini
    # Orchestration needs reliability and coordination
    "ScraperManager": {
        "provider": "openai",
        "model": "gpt-5-mini"
    },
    
    # Multi-Layer ATS - Layer Configuration
    "MultiLayerATS_Layer1": {
        "provider": "deepseek",
        "model": "deepseek-chat"  # Fast baseline
    },
    
    "MultiLayerATS_Layer2": {
        "provider": "openai",
        "model": "gpt-5-mini"  # Validation & refinement
    },
    
    "MultiLayerATS_Layer3": {
        "provider": "deepseek",
        "model": "deepseek-reasoner"  # Detailed feedback
    }
}

# Fallback chain if primary model fails
FALLBACK_CHAIN = [
    "deepseek",  # Try DeepSeek first (fast + cheap)
    "openai",    # Then OpenAI (reliable)
    "gemini",    # Then Gemini (fallback)
    "claude"     # Last resort
]

def get_model_config(agent_name: str) -> dict:
    """
    Get model configuration for specific agent
    
    Args:
        agent_name: Name of the agent class
        
    Returns:
        Dict with provider and model keys
    """
    config = MODEL_ROUTING.get(agent_name)
    
    if not config:
        # Default to OpenAI GPT-5-mini if agent not found
        return {"provider": "openai", "model": "gpt-5-mini"}
    
    return config
