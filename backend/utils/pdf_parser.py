"""
PDF Parser using GPT-5-mini
Extract and parse resume text from PDF files for ATS analysis
"""
from typing import Dict, Optional
import PyPDF2
from io import BytesIO
from ai_agents.base_agent import BaseAgent
from ai_agents.model_config import get_model_config
from utils.logger import setup_logger

logger = setup_logger(__name__)


class PDFParser(BaseAgent):
    """Parse PDF files using GPT-5-mini for intelligent text extraction"""
    
    def __init__(self):
        # Use GPT-5-mini for PDF parsing and extraction
        config = get_model_config('CompanyResearcher')  # GPT-5-mini
        super().__init__(preferred_provider=config["provider"], model=config["model"])
        logger.info("✅ PDF Parser initialized (GPT-5-mini)")
    
    def process(self, pdf_bytes: bytes) -> str:
        """
        Extract and clean text from PDF
        
        Args:
            pdf_bytes: PDF file content as bytes
            
        Returns:
            Cleaned resume text
        """
        try:
            # Extract raw text from PDF
            raw_text = self._extract_raw_text(pdf_bytes)
            
            if not raw_text or len(raw_text.strip()) < 50:
                raise ValueError("PDF appears to be empty or unreadable")
            
            # Use GPT-5-mini to clean and structure the text
            cleaned_text = self._clean_with_ai(raw_text)
            
            logger.info(f"✅ Parsed PDF: {len(raw_text)} → {len(cleaned_text)} chars")
            return cleaned_text
            
        except Exception as e:
            logger.error(f"❌ PDF parsing error: {str(e)}")
            raise
    
    def _extract_raw_text(self, pdf_bytes: bytes) -> str:
        """Extract raw text from PDF using PyPDF2"""
        try:
            pdf_file = BytesIO(pdf_bytes)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            text_parts = []
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text_parts.append(page.extract_text())
            
            raw_text = "\n\n".join(text_parts)
            return raw_text
            
        except Exception as e:
            logger.error(f"❌ Raw PDF extraction failed: {str(e)}")
            raise ValueError(f"Failed to extract text from PDF: {str(e)}")
    
    def _clean_with_ai(self, raw_text: str) -> str:
        """Use GPT-5-mini to clean and structure resume text"""
        
        # If text is already clean enough, return as is
        if len(raw_text) < 5000 and raw_text.count('\n\n') > 5:
            return raw_text
        
        prompt = f"""
Clean and structure this resume text extracted from a PDF.

Remove artifacts, fix formatting issues, and organize sections clearly.
Keep all important information: skills, experience, education, projects.
Use proper line breaks and section headers.

RAW TEXT:
{raw_text[:8000]}

Return ONLY the cleaned resume text, nothing else.
"""
        
        try:
            cleaned = self.generate(prompt, temperature=0.2, max_tokens=3000)
            return cleaned if cleaned else raw_text
        except:
            # If AI cleaning fails, return raw text
            logger.warning("AI cleaning failed, returning raw text")
            return raw_text


class ResumeExtractor(BaseAgent):
    """Extract structured resume information using GPT-5-mini"""
    
    def __init__(self):
        config = get_model_config('CompanyResearcher')  # GPT-5-mini
        super().__init__(preferred_provider=config["provider"], model=config["model"])
    
    def process(self, resume_text: str) -> Dict:
        """
        Extract structured information from resume
        
        Args:
            resume_text: Resume text content
            
        Returns:
            Dictionary with extracted information
        """
        prompt = f"""
Extract key information from this resume in JSON format:

{{
    "skills": ["skill1", "skill2", ...],
    "experience_years": number,
    "job_titles": ["title1", "title2", ...],
    "education": ["degree1", "degree2", ...],
    "technologies": ["tech1", "tech2", ...]
}}

RESUME:
{resume_text[:4000]}

Return only valid JSON, no explanation.
"""
        
        try:
            response = self.generate(prompt, temperature=0.2, max_tokens=1500)
            result = self.parse_json_response(response) if response else {}
            return result or {}
        except Exception as e:
            logger.error(f"Resume extraction error: {str(e)}")
            return {
                "skills": [],
                "experience_years": 0,
                "job_titles": [],
                "education": [],
                "technologies": []
            }
