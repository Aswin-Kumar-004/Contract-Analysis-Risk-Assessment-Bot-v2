from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.units import inch
from datetime import datetime

def export_professional_report(filename, analysis_data):
    """
    Generates a professional PDF report with proper formatting.
    """
    doc = SimpleDocTemplate(filename, pagesize=A4, 
                           rightMargin=72, leftMargin=72,
                           topMargin=72, bottomMargin=18)
    
    styles = getSampleStyleSheet()
    story = []
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1f77b4'),
        spaceAfter=30,
        alignment=1  # Center
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=12,
        spaceBefore=12
    )
    
    # Title
    story.append(Paragraph("Contract Risk Assessment Report", title_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Executive Summary Box
    summary_data = [
        ['Contract Type', analysis_data.get('contract_type', 'Unknown')],
        ['Overall Risk Level', analysis_data.get('overall_risk', 'Unknown')],
        ['High-Risk Clauses', str(analysis_data.get('high_risk_count', 0))],
        ['Medium-Risk Clauses', str(analysis_data.get('medium_risk_count', 0))],
        ['Total Clauses Analyzed', str(analysis_data.get('total_clauses', 0))],
        ['Date of Analysis', datetime.now().strftime('%B %d, %Y')]
    ]
    
    summary_table = Table(summary_data, colWidths=[2.5*inch, 3.5*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8f9fa')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 0.4*inch))
    
    # Financial Impact Section
    if 'financial_impact' in analysis_data:
        story.append(Paragraph("Financial Impact Estimate", heading_style))
        
        financial = analysis_data['financial_impact']
        financial_data = [
            ['Potential Penalty Exposure', f"₹{financial.get('penalty_amount', 0):,.0f}"],
            ['Estimated Business Disruption', f"{financial.get('disruption_days', 0)} days"],
            ['Contract Value (estimated)', f"₹{financial.get('contract_value', 0):,.0f}"]
        ]
        
        financial_table = Table(financial_data, colWidths=[3*inch, 3*inch])
        financial_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#fff3cd')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#ffc107')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        story.append(financial_table)
        story.append(Spacer(1, 0.3*inch))
    
    # High-Risk Clauses Section
    high_risk_clauses = [c for c in analysis_data.get('clauses', []) if c.get('risk') == 'High']
    
    if high_risk_clauses:
        story.append(Paragraph("⚠️ High-Risk Clauses Requiring Immediate Attention", heading_style))
        story.append(Spacer(1, 0.1*inch))
        
        for idx, clause in enumerate(high_risk_clauses, 1):
            # Clause heading
            clause_title = f"{idx}. {clause.get('type', 'Unknown')} Clause (Clause #{clause.get('id', '?')})"
            story.append(Paragraph(clause_title, styles['Heading3']))
            
            # Risk indicator
            risk_para = Paragraph(
                f"<font color='red'><b>RISK LEVEL: HIGH</b></font>",
                styles['BodyText']
            )
            story.append(risk_para)
            story.append(Spacer(1, 0.05*inch))
            
            # Clause text (truncated if too long)
            clause_text = clause.get('text', '')[:400]
            if len(clause.get('text', '')) > 400:
                clause_text += "..."
            
            clause_style = ParagraphStyle(
                'ClauseText',
                parent=styles['BodyText'],
                leftIndent=20,
                fontSize=9,
                textColor=colors.HexColor('#495057'),
                fontName='Helvetica-Oblique'
            )
            story.append(Paragraph(clause_text, clause_style))
            story.append(Spacer(1, 0.1*inch))
            
            # Explanation
            explanation_text = f"<b>Why This Is Risky:</b> {clause.get('explanation', 'Risk assessment unavailable.')}"
            story.append(Paragraph(explanation_text, styles['BodyText']))
            story.append(Spacer(1, 0.05*inch))
            
            # Recommendation
            suggestion_text = f"<b>Recommended Action:</b> {clause.get('suggestion', 'Consult legal counsel.')}"
            story.append(Paragraph(suggestion_text, styles['BodyText']))
            
            # Trigger warnings if available
            if clause.get('triggers'):
                trigger_text = "<b>Specific Issues Found:</b> " + ", ".join([
                    f"'{t.get('keyword', '')}'" for t in clause.get('triggers', [])[:3]
                ])
                story.append(Paragraph(trigger_text, styles['BodyText']))
            
            story.append(Spacer(1, 0.25*inch))
    
    # Medium-Risk Clauses (brief summary)
    medium_risk_clauses = [c for c in analysis_data.get('clauses', []) if c.get('risk') == 'Medium']
    
    if medium_risk_clauses:
        story.append(PageBreak())
        story.append(Paragraph("⚠️ Medium-Risk Clauses for Review", heading_style))
        story.append(Spacer(1, 0.1*inch))
        
        medium_summary = []
        for clause in medium_risk_clauses[:5]:  # Limit to first 5
            medium_summary.append(f"• <b>{clause.get('type', 'Unknown')}</b>: {clause.get('explanation', '')[:150]}...")
        
        for item in medium_summary:
            story.append(Paragraph(item, styles['BodyText']))
            story.append(Spacer(1, 0.05*inch))
    
    # Disclaimer footer
    story.append(PageBreak())
    story.append(Spacer(1, 2*inch))
    
    disclaimer = """
    <b>IMPORTANT DISCLAIMER:</b><br/><br/>
    This report is generated by an AI-powered tool and is for informational purposes only. 
    It does not constitute legal advice and should not be relied upon as a substitute for 
    consultation with a qualified legal professional.<br/><br/>
    
    The analysis is based on pattern matching and machine learning models that may not catch 
    all issues or may flag standard clauses in specific contexts. Always have contracts 
    reviewed by a licensed attorney before signing.<br/><br/>
    
    <b>Generated by Contract Risk Bot</b><br/>
    Powered by Claude AI (Anthropic)<br/>
    Report Date: """ + datetime.now().strftime('%B %d, %Y at %I:%M %p')
    
    disclaimer_style = ParagraphStyle(
        'Disclaimer',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.HexColor('#6c757d'),
        alignment=1  # Center
    )
    story.append(Paragraph(disclaimer, disclaimer_style))
    
    # Build PDF
    doc.build(story)


# Backward compatibility with simple export
def export_report(filename, results):
    """
    Simple export function for backward compatibility.
    """
    analysis_data = {
        'contract_type': 'Unknown',
        'overall_risk': 'Unknown',
        'high_risk_count': sum(1 for r in results if r.get('risk') == 'High'),
        'medium_risk_count': sum(1 for r in results if r.get('risk') == 'Medium'),
        'total_clauses': len(results),
        'clauses': results
    }
    export_professional_report(filename, analysis_data)
