"""
PII Anonymization Utility
Removes personally identifiable information from resume text before sending to LLMs
Uses regex and optional Microsoft Presidio for advanced entity detection
"""
import re
from typing import Dict
from utils.logger import setup_logger

logger = setup_logger(__name__)


class ResumeAnonymizer:
    """
    Scrubs PII (names, phone numbers, emails, addresses) from resume text
    before sending to LLM for analysis
    """
    
    def __init__(self):
        """Initialize anonymizer with regex patterns"""
        # Email pattern
        self.email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        
        # Phone patterns (US/International)
        self.phone_patterns = [
            r'\+?1?\s*\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})',  # US format
            r'\+?[0-9]{1,4}[\s.-]?\(?[0-9]{1,4}\)?[\s.-]?[0-9]{1,4}[\s.-]?[0-9]{1,9}',  # International
            r'\([0-9]{3}\)\s*[0-9]{3}-[0-9]{4}',  # (123) 456-7890
        ]
        
        # Address patterns (street addresses)
        self.address_pattern = r'\d+\s+[A-Za-z0-9\s,\.]+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Lane|Ln|Drive|Dr|Court|Ct|Circle|Cir|Way|Plaza|Square|Sq)\b'
        
        # LinkedIn/Social media URLs
        self.linkedin_pattern = r'https?://(?:www\.)?linkedin\.com/in/[\w-]+'
        self.github_pattern = r'https?://(?:www\.)?github\.com/[\w-]+'
        self.twitter_pattern = r'https?://(?:www\.)?twitter\.com/[\w-]+'
        
        # Names are harder to detect with regex, so we'll use common name section headers
        self.name_section_patterns = [
            r'^([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3})\s*$',  # First line names
            r'Name:\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3})',  # "Name: John Doe"
        ]
        
    def anonymize(self, resume_text: str, keep_skills: bool = True) -> Dict[str, str]:
        """
        Remove PII from resume text
        
        Args:
            resume_text: Original resume text
            keep_skills: Keep technical terms and skills (default True)
            
        Returns:
            Dictionary with:
                - anonymized_text: Scrubbed resume text
                - removed_pii: List of removed items (for logging)
        """
        if not resume_text or not resume_text.strip():
            return {
                "anonymized_text": resume_text,
                "removed_pii": []
            }
        
        original_text = resume_text
        anonymized = resume_text
        removed_items = []
        
        # 1. Remove emails
        emails_found = re.findall(self.email_pattern, anonymized)
        if emails_found:
            anonymized = re.sub(self.email_pattern, '[EMAIL]', anonymized)
            removed_items.extend([f"Email: {email}" for email in emails_found])
            logger.info(f"🔒 Removed {len(emails_found)} email(s)")
        
        # 2. Remove phone numbers (try all patterns)
        phone_count = 0
        for pattern in self.phone_patterns:
            phones_found = re.findall(pattern, anonymized)
            if phones_found:
                anonymized = re.sub(pattern, '[PHONE]', anonymized)
                phone_count += len(phones_found)
        if phone_count > 0:
            removed_items.append(f"Phones: {phone_count} number(s)")
            logger.info(f"🔒 Removed {phone_count} phone number(s)")
        
        # 3. Remove street addresses
        addresses_found = re.findall(self.address_pattern, anonymized, re.IGNORECASE)
        if addresses_found:
            anonymized = re.sub(self.address_pattern, '[ADDRESS]', anonymized, flags=re.IGNORECASE)
            removed_items.extend([f"Address: {addr[:30]}..." for addr in addresses_found])
            logger.info(f"🔒 Removed {len(addresses_found)} address(es)")
        
        # 4. Remove social media URLs
        linkedin_found = re.findall(self.linkedin_pattern, anonymized, re.IGNORECASE)
        if linkedin_found:
            anonymized = re.sub(self.linkedin_pattern, '[LINKEDIN]', anonymized, flags=re.IGNORECASE)
            removed_items.append(f"LinkedIn: {len(linkedin_found)} profile(s)")
            logger.info(f"🔒 Removed LinkedIn profile(s)")
        
        github_found = re.findall(self.github_pattern, anonymized, re.IGNORECASE)
        if github_found:
            anonymized = re.sub(self.github_pattern, '[GITHUB]', anonymized, flags=re.IGNORECASE)
            removed_items.append(f"GitHub: {len(github_found)} profile(s)")
        
        twitter_found = re.findall(self.twitter_pattern, anonymized, re.IGNORECASE)
        if twitter_found:
            anonymized = re.sub(self.twitter_pattern, '[TWITTER]', anonymized, flags=re.IGNORECASE)
            removed_items.append(f"Twitter: {len(twitter_found)} profile(s)")
        
        # 5. Try to detect and remove names from first few lines
        lines = anonymized.split('\n')
        if len(lines) > 0:
            # Check first 3 lines for name-like patterns
            for i in range(min(3, len(lines))):
                line = lines[i].strip()
                # If line looks like a name (2-4 capitalized words, short line)
                if len(line) < 50 and re.match(r'^[A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3}$', line):
                    lines[i] = '[CANDIDATE NAME]'
                    removed_items.append(f"Name: {line}")
                    logger.info(f"🔒 Removed name from header")
                    break
        anonymized = '\n'.join(lines)
        
        # Log summary
        total_removed = len(removed_items)
        logger.info(f"✅ Anonymization complete: {total_removed} PII item(s) removed")
        
        return {
            "anonymized_text": anonymized,
            "removed_pii": removed_items,
            "original_length": len(original_text),
            "anonymized_length": len(anonymized)
        }
    
    def deanonymize_response(self, response_text: str) -> str:
        """
        Replace placeholders in LLM response (if needed for display)
        Currently just returns as-is since we don't store original PII
        """
        return response_text


# Singleton instance
_anonymizer_instance = None

def get_anonymizer() -> ResumeAnonymizer:
    """Get singleton anonymizer instance"""
    global _anonymizer_instance
    if _anonymizer_instance is None:
        _anonymizer_instance = ResumeAnonymizer()
    return _anonymizer_instance
