"""
PDF Export Utility for Manual Prep
Generate professional PDF reports for interview preparation
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from io import BytesIO
import json
from datetime import datetime


def generate_prep_pdf(prep_data: dict) -> BytesIO:
    """
    Generate PDF export of interview preparation
    
    Args:
        prep_data: Dictionary containing all prep information
        
    Returns:
        BytesIO buffer containing PDF data
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
    story = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor='#2563EB',
        spaceAfter=12,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor='#1F2937',
        spaceAfter=10,
        spaceBefore=15
    )
    
    subheading_style = ParagraphStyle(
        'CustomSubheading',
        parent=styles['Heading3'],
        fontSize=12,
        textColor='#374151',
        spaceAfter=8
    )
    
    # Title
    story.append(Paragraph(f"Interview Preparation: {prep_data.get('job_title', 'Position')}", title_style))
    story.append(Paragraph(f"<b>Company:</b> {prep_data.get('company_name', 'N/A')}", styles['Normal']))
    if prep_data.get('job_url'):
        story.append(Paragraph(f"<b>Job URL:</b> {prep_data.get('job_url')}", styles['Normal']))
    story.append(Paragraph(f"<b>Generated:</b> {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}", styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    # Company Insights
    if prep_data.get('company_insights'):
        insights = json.loads(prep_data['company_insights']) if isinstance(prep_data['company_insights'], str) else prep_data['company_insights']
        story.append(Paragraph("Company Insights", heading_style))
        
        if insights.get('overview'):
            story.append(Paragraph(f"<b>Overview:</b> {insights['overview']}", styles['Normal']))
            story.append(Spacer(1, 0.1*inch))
        
        if insights.get('culture'):
            story.append(Paragraph(f"<b>Culture:</b> {insights['culture']}", styles['Normal']))
            story.append(Spacer(1, 0.1*inch))
        
        if insights.get('recent_news'):
            story.append(Paragraph("<b>Recent News:</b>", styles['Normal']))
            for news in insights['recent_news'][:3]:
                story.append(Paragraph(f"\u2022 {news}", styles['Normal']))
            story.append(Spacer(1, 0.1*inch))
    
    # Key Talking Points
    if prep_data.get('key_talking_points'):
        points = json.loads(prep_data['key_talking_points']) if isinstance(prep_data['key_talking_points'], str) else prep_data['key_talking_points']
        story.append(PageBreak())
        story.append(Paragraph("Key Talking Points", heading_style))
        
        for point in points:
            story.append(Paragraph(f"<b>\u2605 {point.get('point', '')}</b>", subheading_style))
            story.append(Paragraph(f"Why: {point.get('why', '')}", styles['Normal']))
            if point.get('how_to_mention'):
                story.append(Paragraph(f"When to mention: {point.get('how_to_mention', '')}", styles['Normal']))
            story.append(Spacer(1, 0.15*inch))
    
    # Technical Q&A
    if prep_data.get('technical_qa'):
        qa_list = json.loads(prep_data['technical_qa']) if isinstance(prep_data['technical_qa'], str) else prep_data['technical_qa']
        story.append(PageBreak())
        story.append(Paragraph("Technical Questions & Answers", heading_style))
        
        for i, qa in enumerate(qa_list[:10], 1):
            story.append(Paragraph(f"<b>Q{i}: {qa.get('question', '')}</b>", subheading_style))
            if qa.get('difficulty'):
                story.append(Paragraph(f"Difficulty: {qa['difficulty']}", styles['Normal']))
            story.append(Paragraph(f"<b>Answer:</b> {qa.get('answer', '')}", styles['Normal']))
            if qa.get('follow_up'):
                story.append(Paragraph(f"<i>Follow-up: {qa['follow_up']}</i>", styles['Normal']))
            story.append(Spacer(1, 0.2*inch))
    
    # Behavioral Q&A
    if prep_data.get('behavioral_qa'):
        qa_list = json.loads(prep_data['behavioral_qa']) if isinstance(prep_data['behavioral_qa'], str) else prep_data['behavioral_qa']
        story.append(PageBreak())
        story.append(Paragraph("Behavioral Questions (STAR Method)", heading_style))
        
        for i, qa in enumerate(qa_list[:8], 1):
            story.append(Paragraph(f"<b>Q{i}: {qa.get('question', '')}</b>", subheading_style))
            if qa.get('star_example'):
                star = qa['star_example']
                story.append(Paragraph(f"<b>Situation:</b> {star.get('situation', '')}", styles['Normal']))
                story.append(Paragraph(f"<b>Task:</b> {star.get('task', '')}", styles['Normal']))
                story.append(Paragraph(f"<b>Action:</b> {star.get('action', '')}", styles['Normal']))
                story.append(Paragraph(f"<b>Result:</b> {star.get('result', '')}", styles['Normal']))
            if qa.get('key_takeaway'):
                story.append(Paragraph(f"<i>Key Takeaway: {qa['key_takeaway']}</i>", styles['Normal']))
            story.append(Spacer(1, 0.2*inch))
    
    # HR Q&A
    if prep_data.get('hr_qa'):
        qa_list = json.loads(prep_data['hr_qa']) if isinstance(prep_data['hr_qa'], str) else prep_data['hr_qa']
        story.append(PageBreak())
        story.append(Paragraph("HR & Salary Questions", heading_style))
        
        for i, qa in enumerate(qa_list[:6], 1):
            story.append(Paragraph(f"<b>Q{i}: {qa.get('question', '')}</b>", subheading_style))
            story.append(Paragraph(f"<b>Answer Strategy:</b> {qa.get('answer', '')}", styles['Normal']))
            if qa.get('tips'):
                story.append(Paragraph("<b>Tips:</b>", styles['Normal']))
                for tip in qa['tips'][:3]:
                    story.append(Paragraph(f"\u2022 {tip}", styles['Normal']))
            story.append(Spacer(1, 0.2*inch))
    
    # Preparation Tips
    if prep_data.get('preparation_tips'):
        tips = json.loads(prep_data['preparation_tips']) if isinstance(prep_data['preparation_tips'], str) else prep_data['preparation_tips']
        story.append(PageBreak())
        story.append(Paragraph("Preparation Tips", heading_style))
        
        for tip in tips:
            priority = tip.get('priority', 'Medium')
            story.append(Paragraph(f"<b>[{priority}] {tip.get('tip', '')}</b>", subheading_style))
            story.append(Paragraph(f"Category: {tip.get('category', 'General')}", styles['Normal']))
            story.append(Spacer(1, 0.15*inch))
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer
