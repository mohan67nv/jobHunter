"""
Base AI Agent class
Provides common functionality for all AI agents with multi-provider support
"""
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
import json
from config import settings
from utils.logger import setup_logger

logger = setup_logger(__name__)

# Import AI providers
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

try:
    from anthropic import Anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


class BaseAgent(ABC):
    """Abstract base class for AI agents"""
    
    def __init__(self, preferred_provider: str = "gemini"):
        """
        Initialize AI agent
        
        Args:
            preferred_provider: Preferred AI provider (gemini, claude, openai)
        """
        self.preferred_provider = preferred_provider
        self.providers = self._initialize_providers()
        
        if not self.providers:
            logger.error("❌ No AI providers available! Please configure API keys.")
    
    def _initialize_providers(self) -> Dict[str, Any]:
        """Initialize available AI providers"""
        providers = {}
        
        # Gemini
        if GEMINI_AVAILABLE and settings.gemini_api_key:
            try:
                genai.configure(api_key=settings.gemini_api_key)
                providers['gemini'] = genai.GenerativeModel('gemini-pro')
                logger.info("✅ Gemini Pro initialized")
            except Exception as e:
                logger.error(f"Failed to initialize Gemini: {e}")
        
        # Claude
        if ANTHROPIC_AVAILABLE and settings.anthropic_api_key:
            try:
                providers['claude'] = Anthropic(api_key=settings.anthropic_api_key)
                logger.info("✅ Claude initialized")
            except Exception as e:
                logger.error(f"Failed to initialize Claude: {e}")
        
        # OpenAI
        if OPENAI_AVAILABLE and settings.openai_api_key:
            try:
                providers['openai'] = OpenAI(api_key=settings.openai_api_key)
                logger.info("✅ OpenAI initialized")
            except Exception as e:
                logger.error(f"Failed to initialize OpenAI: {e}")
        
        return providers
    
    def generate(self, prompt: str, temperature: float = 0.7, max_tokens: int = 2000) -> Optional[str]:
        """
        Generate response using available AI provider
        
        Args:
            prompt: Input prompt
            temperature: Sampling temperature (0-1)
            max_tokens: Maximum tokens in response
            
        Returns:
            Generated text or None if all providers fail
        """
        # Try preferred provider first
        if self.preferred_provider in self.providers:
            result = self._try_provider(self.preferred_provider, prompt, temperature, max_tokens)
            if result:
                return result
        
        # Fallback to other providers
        for provider_name in self.providers:
            if provider_name != self.preferred_provider:
                result = self._try_provider(provider_name, prompt, temperature, max_tokens)
                if result:
                    logger.info(f"Fallback to {provider_name} successful")
                    return result
        
        logger.error("❌ All AI providers failed")
        return None
    
    def _try_provider(self, provider_name: str, prompt: str, 
                     temperature: float, max_tokens: int) -> Optional[str]:
        """Try to generate response with specific provider"""
        try:
            if provider_name == 'gemini':
                return self._generate_gemini(prompt, temperature, max_tokens)
            elif provider_name == 'claude':
                return self._generate_claude(prompt, temperature, max_tokens)
            elif provider_name == 'openai':
                return self._generate_openai(prompt, temperature, max_tokens)
        except Exception as e:
            logger.error(f"Error with {provider_name}: {e}")
            return None
    
    def _generate_gemini(self, prompt: str, temperature: float, max_tokens: int) -> str:
        """Generate response using Gemini"""
        model = self.providers['gemini']
        
        generation_config = {
            'temperature': temperature,
            'max_output_tokens': max_tokens,
        }
        
        response = model.generate_content(
            prompt,
            generation_config=generation_config
        )
        
        return response.text
    
    def _generate_claude(self, prompt: str, temperature: float, max_tokens: int) -> str:
        """Generate response using Claude"""
        client = self.providers['claude']
        
        message = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=max_tokens,
            temperature=temperature,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        return message.content[0].text
    
    def _generate_openai(self, prompt: str, temperature: float, max_tokens: int) -> str:
        """Generate response using OpenAI"""
        client = self.providers['openai']
        
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        return response.choices[0].message.content
    
    def parse_json_response(self, response: str) -> Optional[Dict]:
        """
        Parse JSON from AI response
        
        Args:
            response: AI-generated text
            
        Returns:
            Parsed JSON dict or None if parsing fails
        """
        try:
            # Try to find JSON in response (sometimes wrapped in markdown)
            if '```json' in response:
                json_str = response.split('```json')[1].split('```')[0].strip()
            elif '```' in response:
                json_str = response.split('```')[1].strip()
            else:
                json_str = response.strip()
            
            return json.loads(json_str)
        except Exception as e:
            logger.error(f"Error parsing JSON response: {e}")
            logger.debug(f"Response was: {response[:500]}")
            return None
    
    @abstractmethod
    def process(self, *args, **kwargs) -> Dict:
        """
        Process input and return results
        Must be implemented by subclasses
        """
        pass
