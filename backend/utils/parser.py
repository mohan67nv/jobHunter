"""
Resume and document parsing utilities
Extracts text from PDF and DOCX files
"""
from typing import Optional
import os
from utils.logger import setup_logger

try:
    from PyPDF2 import PdfReader
    PYPDF2_AVAILABLE = True
except ImportError:
    PYPDF2_AVAILABLE = False

try:
    from docx import Document
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False

logger = setup_logger(__name__)


class TextExtractor:
    """Extract text from various document formats"""
    
    @staticmethod
    def extract_from_pdf(file_path: str) -> Optional[str]:
        """
        Extract text from PDF file
        
        Args:
            file_path: Path to PDF file
            
        Returns:
            Extracted text or None if error
        """
        if not PYPDF2_AVAILABLE:
            logger.error("PyPDF2 not installed")
            return None
        
        try:
            reader = PdfReader(file_path)
            text = ""
            
            for page in reader.pages:
                text += page.extract_text() + "\n"
            
            return text.strip()
        
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {e}")
            return None
    
    @staticmethod
    def extract_from_docx(file_path: str) -> Optional[str]:
        """
        Extract text from DOCX file
        
        Args:
            file_path: Path to DOCX file
            
        Returns:
            Extracted text or None if error
        """
        if not DOCX_AVAILABLE:
            logger.error("python-docx not installed")
            return None
        
        try:
            doc = Document(file_path)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return text.strip()
        
        except Exception as e:
            logger.error(f"Error extracting text from DOCX: {e}")
            return None
    
    @staticmethod
    def extract_from_file(file_path: str) -> Optional[str]:
        """
        Auto-detect format and extract text
        
        Args:
            file_path: Path to file
            
        Returns:
            Extracted text or None if error
        """
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            return None
        
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext == '.pdf':
            return TextExtractor.extract_from_pdf(file_path)
        elif ext == '.docx':
            return TextExtractor.extract_from_docx(file_path)
        elif ext == '.txt':
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
            except Exception as e:
                logger.error(f"Error reading text file: {e}")
                return None
        else:
            logger.error(f"Unsupported file format: {ext}")
            return None


class ResumeParser:
    """Parse and extract information from resumes"""
    
    def __init__(self):
        self.extractor = TextExtractor()
    
    def parse_resume(self, file_path: str) -> dict:
        """
        Parse resume file and extract structured information
        
        Args:
            file_path: Path to resume file
            
        Returns:
            Dictionary with extracted information
        """
        logger.info(f"Parsing resume: {file_path}")
        
        # Extract text
        text = self.extractor.extract_from_file(file_path)
        
        if not text:
            return {
                'text': '',
                'error': 'Failed to extract text from file'
            }
        
        # Extract basic information
        result = {
            'text': text,
            'skills': self._extract_skills(text),
            'experience_years': self._estimate_experience(text),
            'education': self._extract_education(text),
            'contact': self._extract_contact(text),
        }
        
        logger.info(f"Resume parsed: {len(result['skills'])} skills found")
        
        return result
    
    def _extract_skills(self, text: str) -> list:
        """Extract technical skills from resume text"""
        text_lower = text.lower()
        
        # Common technical skills (can be expanded)
        skill_keywords = [
            'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'ruby', 'go', 'rust',
            'sql', 'nosql', 'postgresql', 'mysql', 'mongodb', 'redis',
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform',
            'react', 'angular', 'vue', 'node.js', 'django', 'flask', 'spring',
            'machine learning', 'deep learning', 'tensorflow', 'pytorch', 'scikit-learn',
            'data science', 'data analysis', 'pandas', 'numpy', 'matplotlib',
            'git', 'ci/cd', 'jenkins', 'gitlab', 'github actions',
            'agile', 'scrum', 'jira', 'confluence',
            'rest api', 'graphql', 'microservices', 'distributed systems',
        ]
        
        found_skills = []
        for skill in skill_keywords:
            if skill in text_lower:
                found_skills.append(skill.title())
        
        return found_skills
    
    def _estimate_experience(self, text: str) -> int:
        """Estimate years of experience from resume"""
        import re
        
        # Look for patterns like "5 years", "5+ years", "2019-2023"
        year_patterns = [
            r'(\d+)\+?\s*years?\s+(?:of\s+)?experience',
            r'experience[:\s]+(\d+)\+?\s*years?',
        ]
        
        for pattern in year_patterns:
            match = re.search(pattern, text.lower())
            if match:
                return int(match.group(1))
        
        # Count date ranges (rough estimate)
        date_ranges = re.findall(r'(\d{4})\s*[-–]\s*(\d{4}|present|current)', text.lower())
        if date_ranges:
            total_years = 0
            for start, end in date_ranges:
                end_year = 2024 if end in ['present', 'current'] else int(end)
                total_years += max(0, end_year - int(start))
            return min(total_years, 30)  # Cap at 30 years
        
        return 0
    
    def _extract_education(self, text: str) -> list:
        """Extract education information"""
        import re
        
        education = []
        
        # Look for degree keywords
        degree_keywords = [
            'bachelor', 'master', 'phd', 'doctorate', 'mba', 'bsc', 'msc',
            'b.s.', 'm.s.', 'b.a.', 'm.a.'
        ]
        
        lines = text.split('\n')
        for line in lines:
            line_lower = line.lower()
            for degree in degree_keywords:
                if degree in line_lower:
                    education.append(line.strip())
                    break
        
        return education
    
    def _extract_contact(self, text: str) -> dict:
        """Extract contact information"""
        import re
        
        contact = {}
        
        # Email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        email_match = re.search(email_pattern, text)
        if email_match:
            contact['email'] = email_match.group(0)
        
        # Phone (simple pattern)
        phone_pattern = r'\+?\d{1,4}[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}'
        phone_match = re.search(phone_pattern, text)
        if phone_match:
            contact['phone'] = phone_match.group(0)
        
        # LinkedIn
        linkedin_pattern = r'linkedin\.com/in/[\w-]+'
        linkedin_match = re.search(linkedin_pattern, text.lower())
        if linkedin_match:
            contact['linkedin'] = 'https://' + linkedin_match.group(0)
        
        # GitHub
        github_pattern = r'github\.com/[\w-]+'
        github_match = re.search(github_pattern, text.lower())
        if github_match:
            contact['github'] = 'https://' + github_match.group(0)
        
        return contact
