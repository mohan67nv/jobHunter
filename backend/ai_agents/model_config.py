"""
Centralized AI Model Configuration
Maps each agent to its optimal model based on task requirements and cost efficiency

DeepSeek Models Strategy:
- deepseek-coder: Code/parsing, structured data extraction (JD parsing, resume optimization)
- deepseek-chat (V3): Analysis, matching, scoring (ATS, matching, web scraping)
- deepseek-reasoner (R1): Complex reasoning, interview prep, behavioral analysis
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
    
    # ATS Scoring - DeepSeek V3 (Chat)
    # Fast keyword analysis and scoring
    "EnhancedATSScorer": {
        "provider": "deepseek",
        "model": "deepseek-chat"
    },
    
    "ATSScorer": {
        "provider": "deepseek",
        "model": "deepseek-chat"
    },
    
    # Company Research - DeepSeek Reasoner (R1)
    # Complex reasoning for interview prep, behavioral Q&A analysis
    "CompanyResearcher": {
        "provider": "deepseek",
        "model": "deepseek-reasoner"
    },
    
    # Web Scraping - DeepSeek Reasoner (R1)
    # Complex pattern recognition, intelligent content extraction from job sites
    "AIJobScraper": {
        "provider": "deepseek",
        "model": "deepseek-reasoner"
    },
    
    # Scraper Manager - DeepSeek Chat (V3)
    # General scraping coordination and data processing
    "ScraperManager": {
        "provider": "deepseek",
        "model": "deepseek-chat"
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
