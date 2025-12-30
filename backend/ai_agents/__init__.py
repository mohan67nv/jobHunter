"""
AI Agents package for SmartJobHunter Pro
Intelligent job analysis using Gemini Pro, Claude, or GPT-4
"""
from ai_agents.base_agent import BaseAgent
from ai_agents.jd_analyzer import JDAnalyzer
from ai_agents.matcher import ResumeMatcher
from ai_agents.ats_scorer import ATSScorer
from ai_agents.optimizer import ApplicationOptimizer
from ai_agents.researcher import CompanyResearcher
from ai_agents.agent_manager import AgentManager

__all__ = [
    "BaseAgent",
    "JDAnalyzer",
    "ResumeMatcher",
    "ATSScorer",
    "ApplicationOptimizer",
    "CompanyResearcher",
    "AgentManager",
]
