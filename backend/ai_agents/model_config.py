"""
Centralized AI Model Configuration
Maps each agent to its optimal model based on task requirements and cost efficiency
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
    
    # Company Research - GPT-5-mini
    # Knowledge-heavy task, benefits from OpenAI's training
    "CompanyResearcher": {
        "provider": "openai",
        "model": "gpt-5-mini"
    },
    
    # Web Scraping - DeepSeek V3 (Chat)
    # Pattern recognition and content extraction
    "AIJobScraper": {
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
