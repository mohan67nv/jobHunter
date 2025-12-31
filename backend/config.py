"""
Configuration management for SmartJobHunter Pro
Loads settings from environment variables
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Database
    database_url: str = "sqlite:///data/jobhunter.db"
    
    # Application
    secret_key: str = "change-this-in-production"
    environment: str = "development"
    debug: bool = True
    
    # AI API Keys
    gemini_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None
    perplexity_api_key: Optional[str] = None
    rovodev_api_key: Optional[str] = None
    
    # Scraping Configuration
    user_agent: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    scrape_delay_min: int = 2
    scrape_delay_max: int = 5
    max_jobs_per_source: int = 500
    max_total_jobs: int = 5000  # Maximum jobs to store in database
    
    # Scheduler
    scrape_interval_hours: int = 2  # Auto-scrape every 2 hours
    analysis_interval_hours: int = 2  # Analyze every 2 hours
    
    # Email Notifications
    email_enabled: bool = False
    email_host: str = "smtp.gmail.com"
    email_port: int = 587
    email_user: Optional[str] = None
    email_password: Optional[str] = None
    email_from: str = "SmartJobHunter <noreply@jobhunter.local>"
    
    # Telegram Notifications
    telegram_enabled: bool = False
    telegram_bot_token: Optional[str] = None
    telegram_chat_id: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
