"""
PDF generator for tailored resumes and cover letters
Creates formatted PDF documents
"""
from typing import Optional
import os
from datetime import datetime
from utils.logger import setup_logger

try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
    from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

logger = setup_logger(__name__)


class PDFGenerator:
    """Generates PDF documents for resumes and cover letters"""
    
    def __init__(self):
        if not REPORTLAB_AVAILABLE:
            logger.warning("⚠️  ReportLab not installed. PDF generation unavailable.")
        
        self.styles = getSampleStyleSheet() if REPORTLAB_AVAILABLE else None
    
    def generate_resume(self, content: str, output_path: str, user_info: dict = None) -> bool:
        """
        Generate tailored resume PDF
        
        Args:
            content: Resume content (text with formatting)
            output_path: Path to save PDF
            user_info: Dictionary with user information (name, email, phone, etc.)
            
        Returns:
            True if successful, False otherwise
        """
        if not REPORTLAB_AVAILABLE:
            logger.error("ReportLab not available")
            return False
        
        try:
            # Ensure output directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            doc = SimpleDocTemplate(output_path, pagesize=letter)
            story = []
            
            # Custom styles
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=self.styles['Heading1'],
                fontSize=24,
                textColor='#2563eb',
                spaceAfter=6,
                alignment=TA_CENTER
            )
            
            heading_style = ParagraphStyle(
                'CustomHeading',
                parent=self.styles['Heading2'],
                fontSize=14,
                textColor='#1e40af',
                spaceAfter=6,
                spaceBefore=12
            )
            
            normal_style = self.styles['Normal']
            
            # Add user header if provided
            if user_info:
                name = user_info.get('name', '')
                if name:
                    story.append(Paragraph(name, title_style))
                    story.append(Spacer(1, 0.1 * inch))
                
                contact_info = []
                if user_info.get('email'):
                    contact_info.append(user_info['email'])
                if user_info.get('phone'):
                    contact_info.append(user_info['phone'])
                if user_info.get('linkedin_url'):
                    contact_info.append(user_info['linkedin_url'])
                
                if contact_info:
                    contact_text = ' | '.join(contact_info)
                    contact_style = ParagraphStyle(
                        'Contact',
                        parent=self.styles['Normal'],
                        fontSize=10,
                        alignment=TA_CENTER
                    )
                    story.append(Paragraph(contact_text, contact_style))
                    story.append(Spacer(1, 0.2 * inch))
            
            # Parse and add content
            lines = content.split('\n')
            
            for line in lines:
                line = line.strip()
                
                if not line:
                    story.append(Spacer(1, 0.1 * inch))
                    continue
                
                # Detect headings (all caps or starts with ##)
                if line.isupper() or line.startswith('##'):
                    heading_text = line.replace('##', '').strip()
                    story.append(Paragraph(heading_text, heading_style))
                elif line.startswith('- ') or line.startswith('• '):
                    bullet_text = line[2:].strip()
                    story.append(Paragraph(f"• {bullet_text}", normal_style))
                else:
                    story.append(Paragraph(line, normal_style))
            
            # Build PDF
            doc.build(story)
            
            logger.info(f"✅ Resume PDF generated: {output_path}")
            return True
        
        except Exception as e:
            logger.error(f"❌ Error generating resume PDF: {e}")
            return False
    
    def generate_cover_letter(self, content: str, output_path: str, 
                             user_info: dict = None, job_info: dict = None) -> bool:
        """
        Generate cover letter PDF
        
        Args:
            content: Cover letter content
            output_path: Path to save PDF
            user_info: User information
            job_info: Job information (title, company)
            
        Returns:
            True if successful, False otherwise
        """
        if not REPORTLAB_AVAILABLE:
            logger.error("ReportLab not available")
            return False
        
        try:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            doc = SimpleDocTemplate(output_path, pagesize=letter)
            story = []
            
            normal_style = self.styles['Normal']
            
            # Add date
            date_str = datetime.now().strftime('%B %d, %Y')
            story.append(Paragraph(date_str, normal_style))
            story.append(Spacer(1, 0.2 * inch))
            
            # Add user info
            if user_info:
                if user_info.get('name'):
                    story.append(Paragraph(user_info['name'], normal_style))
                if user_info.get('email'):
                    story.append(Paragraph(user_info['email'], normal_style))
                if user_info.get('phone'):
                    story.append(Paragraph(user_info['phone'], normal_style))
                story.append(Spacer(1, 0.2 * inch))
            
            # Add recipient info
            if job_info:
                if job_info.get('company'):
                    story.append(Paragraph(f"Hiring Manager", normal_style))
                    story.append(Paragraph(job_info['company'], normal_style))
                story.append(Spacer(1, 0.2 * inch))
            
            # Add content
            paragraphs = content.split('\n\n')
            
            for para in paragraphs:
                if para.strip():
                    story.append(Paragraph(para.strip(), normal_style))
                    story.append(Spacer(1, 0.15 * inch))
            
            # Add signature
            story.append(Spacer(1, 0.2 * inch))
            story.append(Paragraph("Sincerely,", normal_style))
            story.append(Spacer(1, 0.3 * inch))
            if user_info and user_info.get('name'):
                story.append(Paragraph(user_info['name'], normal_style))
            
            # Build PDF
            doc.build(story)
            
            logger.info(f"✅ Cover letter PDF generated: {output_path}")
            return True
        
        except Exception as e:
            logger.error(f"❌ Error generating cover letter PDF: {e}")
            return False
    
    def generate_job_report(self, job_data: dict, analysis_data: dict, output_path: str) -> bool:
        """
        Generate job analysis report PDF
        
        Args:
            job_data: Job information
            analysis_data: AI analysis results
            output_path: Path to save PDF
            
        Returns:
            True if successful, False otherwise
        """
        if not REPORTLAB_AVAILABLE:
            logger.error("ReportLab not available")
            return False
        
        try:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            doc = SimpleDocTemplate(output_path, pagesize=letter)
            story = []
            
            title_style = ParagraphStyle(
                'ReportTitle',
                parent=self.styles['Heading1'],
                fontSize=18,
                spaceAfter=12
            )
            
            heading_style = self.styles['Heading2']
            normal_style = self.styles['Normal']
            
            # Title
            story.append(Paragraph("Job Analysis Report", title_style))
            story.append(Spacer(1, 0.2 * inch))
            
            # Job info
            story.append(Paragraph(f"<b>{job_data.get('title', 'N/A')}</b>", heading_style))
            story.append(Paragraph(f"{job_data.get('company', 'N/A')} - {job_data.get('location', 'N/A')}", normal_style))
            story.append(Spacer(1, 0.2 * inch))
            
            # Match scores
            story.append(Paragraph("<b>Match Score:</b>", heading_style))
            story.append(Paragraph(f"Overall Match: {analysis_data.get('match_score', 0):.0f}%", normal_style))
            story.append(Paragraph(f"ATS Score: {analysis_data.get('ats_score', 0):.0f}%", normal_style))
            story.append(Spacer(1, 0.2 * inch))
            
            # Matching skills
            if analysis_data.get('matching_skills'):
                story.append(Paragraph("<b>Matching Skills:</b>", heading_style))
                for skill in analysis_data['matching_skills'][:10]:
                    story.append(Paragraph(f"✓ {skill}", normal_style))
                story.append(Spacer(1, 0.2 * inch))
            
            # Missing skills
            if analysis_data.get('missing_skills'):
                story.append(Paragraph("<b>Skills to Develop:</b>", heading_style))
                for skill in analysis_data['missing_skills'][:10]:
                    story.append(Paragraph(f"○ {skill}", normal_style))
                story.append(Spacer(1, 0.2 * inch))
            
            # Build PDF
            doc.build(story)
            
            logger.info(f"✅ Job report PDF generated: {output_path}")
            return True
        
        except Exception as e:
            logger.error(f"❌ Error generating job report PDF: {e}")
            return False
