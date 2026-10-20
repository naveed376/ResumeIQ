from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import io

class ReportGenerator:
    """Generate professional PDF report."""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a1a2e'),
            spaceAfter=30
        )
        
        self.heading_style = ParagraphStyle(
            'CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#16213e'),
            spaceAfter=10
        )
        
        self.body_style = ParagraphStyle(
            'CustomBody',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.black,
            spaceAfter=8
        )
    
    def generate_report(self, analysis_result, resume_text, job_description):
        """Generate PDF report."""
        buffer = io.BytesIO()
        
        # Create PDF
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        story = []
        
        # Title
        story.append(Paragraph("Resume Analysis Report", self.title_style))
        story.append(Spacer(1, 12))
        
        # Match Score
        score = analysis_result.get('match_score', 0)
        story.append(Paragraph(f"Match Score: {score}/100", self.heading_style))
        story.append(Spacer(1, 6))
        
        # Summary
        summary = analysis_result.get('summary', 'No summary available')
        story.append(Paragraph(f"<b>Summary:</b> {summary}", self.body_style))
        story.append(Spacer(1, 12))
        
        # Missing Skills
        missing = analysis_result.get('missing_skills', [])
        if missing:
            story.append(Paragraph("Missing Skills", self.heading_style))
            for skill in missing:
                story.append(Paragraph(f"• {skill}", self.body_style))
            story.append(Spacer(1, 12))
        
        # Strengths
        strengths = analysis_result.get('strengths', [])
        if strengths:
            story.append(Paragraph("Strengths", self.heading_style))
            for strength in strengths:
                story.append(Paragraph(f"• {strength}", self.body_style))
            story.append(Spacer(1, 12))
        
        # Recommendations
        recommendations = analysis_result.get('recommendations', [])
        if recommendations:
            story.append(Paragraph("Recommendations", self.heading_style))
            for rec in recommendations:
                story.append(Paragraph(f"• {rec}", self.body_style))
            story.append(Spacer(1, 12))
        
        doc.build(story)
        buffer.seek(0)
        
        return buffer