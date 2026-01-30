"""
PDF Report Generator for ProcBench Analysis Results

Generates comprehensive PDF reports containing:
- Executive summary with key findings
- Risk distribution charts
- Detailed process analysis
- Timeline of suspicious activities
- AI-generated insights
"""

import io
import logging
from datetime import datetime
from typing import Any, Optional

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
    Image,
    ListFlowable,
    ListItem,
)
from reportlab.graphics.shapes import Drawing, Rect, String
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.barcharts import VerticalBarChart

logger = logging.getLogger(__name__)


class PDFGenerator:
    """
    Generates PDF reports from analysis results.
    
    Attributes:
        styles: ReportLab paragraph styles
        page_size: PDF page dimensions
    """
    
    def __init__(self, page_size: tuple = letter):
        """
        Initialize PDF generator.
        
        Args:
            page_size: Page dimensions (default: letter)
        """
        self.page_size = page_size
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self) -> None:
        """Configure custom paragraph styles for the report."""
        # Title style
        self.styles.add(ParagraphStyle(
            name='ReportTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=1,  # Center
            textColor=colors.HexColor('#1a1a2e'),
        ))
        
        # Section header style
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceBefore=20,
            spaceAfter=10,
            textColor=colors.HexColor('#16213e'),
            borderPadding=5,
        ))
        
        # Subsection style
        self.styles.add(ParagraphStyle(
            name='Subsection',
            parent=self.styles['Heading3'],
            fontSize=12,
            spaceBefore=15,
            spaceAfter=8,
            textColor=colors.HexColor('#0f3460'),
        ))
        
        # Custom body text style (BodyText already exists in sample styles)
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceBefore=4,
            spaceAfter=4,
            leading=14,
        ))
        
        # High risk text
        self.styles.add(ParagraphStyle(
            name='HighRisk',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#e63946'),
            fontName='Helvetica-Bold',
        ))
        
        # Medium risk text
        self.styles.add(ParagraphStyle(
            name='MediumRisk',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#f4a261'),
            fontName='Helvetica-Bold',
        ))
        
        # Low risk text
        self.styles.add(ParagraphStyle(
            name='LowRisk',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#2a9d8f'),
        ))
    
    def generate(self, analysis_result: dict) -> bytes:
        """
        Generate a PDF report from analysis results.
        
        Args:
            analysis_result: Complete analysis result dictionary
            
        Returns:
            PDF file contents as bytes
        """
        buffer = io.BytesIO()
        
        doc = SimpleDocTemplate(
            buffer,
            pagesize=self.page_size,
            rightMargin=0.75 * inch,
            leftMargin=0.75 * inch,
            topMargin=0.75 * inch,
            bottomMargin=0.75 * inch,
        )
        
        # Build document elements
        elements = []
        
        # Title page
        elements.extend(self._create_title_page(analysis_result))
        elements.append(PageBreak())
        
        # Executive summary
        elements.extend(self._create_executive_summary(analysis_result))
        elements.append(PageBreak())
        
        # Risk distribution
        elements.extend(self._create_risk_distribution(analysis_result))
        
        # Top threats
        elements.extend(self._create_top_threats(analysis_result))
        elements.append(PageBreak())
        
        # Detailed findings
        elements.extend(self._create_detailed_findings(analysis_result))
        
        # Build PDF
        doc.build(elements, onFirstPage=self._add_header_footer, 
                  onLaterPages=self._add_header_footer)
        
        buffer.seek(0)
        return buffer.getvalue()
    
    def _create_title_page(self, result: dict) -> list:
        """Create the title page elements."""
        elements = []
        
        # Add spacer for vertical centering
        elements.append(Spacer(1, 2 * inch))
        
        # Title
        elements.append(Paragraph(
            "ProcBench Analysis Report",
            self.styles['ReportTitle']
        ))
        
        elements.append(Spacer(1, 0.5 * inch))
        
        # Subtitle with filename
        filename = result.get('filename', 'Unknown File')
        elements.append(Paragraph(
            f"<b>Analyzed File:</b> {filename}",
            ParagraphStyle(
                name='Subtitle',
                parent=self.styles['Normal'],
                fontSize=14,
                alignment=1,
            )
        ))
        
        elements.append(Spacer(1, 0.3 * inch))
        
        # Generation timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        elements.append(Paragraph(
            f"<b>Generated:</b> {timestamp}",
            ParagraphStyle(
                name='Timestamp',
                parent=self.styles['Normal'],
                fontSize=11,
                alignment=1,
            )
        ))
        
        elements.append(Spacer(1, 0.3 * inch))
        
        # Analysis ID
        analysis_id = result.get('analysis_id', 'N/A')
        elements.append(Paragraph(
            f"<b>Analysis ID:</b> {analysis_id}",
            ParagraphStyle(
                name='AnalysisID',
                parent=self.styles['Normal'],
                fontSize=11,
                alignment=1,
            )
        ))
        
        elements.append(Spacer(1, 1 * inch))
        
        # Quick stats box
        elements.extend(self._create_quick_stats(result))
        
        return elements
    
    def _create_quick_stats(self, result: dict) -> list:
        """Create quick statistics summary box."""
        elements = []
        
        total_events = result.get('total_events', 0)
        total_processes = result.get('total_processes', 0)
        flagged = result.get('flagged_processes', 0)
        high_risk = result.get('high_risk_count', 0)
        medium_risk = result.get('medium_risk_count', 0)
        
        # Create stats table
        data = [
            ['Total Events', 'Total Processes', 'Flagged', 'High Risk', 'Medium Risk'],
            [str(total_events), str(total_processes), str(flagged), str(high_risk), str(medium_risk)]
        ]
        
        table = Table(data, colWidths=[1.3 * inch] * 5)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#16213e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('FONTSIZE', (0, 1), (-1, 1), 14),
            ('FONTNAME', (0, 1), (-1, 1), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 1), (-1, 1), 12),
            ('BOTTOMPADDING', (0, 1), (-1, 1), 12),
            ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#f0f0f0')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cccccc')),
            # Highlight high risk count if > 0
            ('TEXTCOLOR', (3, 1), (3, 1), colors.HexColor('#e63946') if high_risk > 0 else colors.black),
            # Highlight medium risk if > 0
            ('TEXTCOLOR', (4, 1), (4, 1), colors.HexColor('#f4a261') if medium_risk > 0 else colors.black),
        ]))
        
        elements.append(table)
        
        return elements
    
    def _create_executive_summary(self, result: dict) -> list:
        """Create executive summary section."""
        elements = []
        
        elements.append(Paragraph("Executive Summary", self.styles['SectionHeader']))
        
        # Analysis overview
        total_events = result.get('total_events', 0)
        total_processes = result.get('total_processes', 0)
        flagged = result.get('flagged_processes', 0)
        duration = result.get('analysis_duration_seconds', 0)
        
        summary_text = f"""
        This report presents the analysis of Process Monitor log data containing 
        <b>{total_events:,}</b> events across <b>{total_processes}</b> unique processes. 
        The analysis was completed in <b>{duration:.2f} seconds</b>.
        """
        elements.append(Paragraph(summary_text, self.styles['CustomBody']))
        
        elements.append(Spacer(1, 0.2 * inch))
        
        # Key findings
        elements.append(Paragraph("Key Findings", self.styles['Subsection']))
        
        high_risk = result.get('high_risk_count', 0)
        medium_risk = result.get('medium_risk_count', 0)
        low_risk = result.get('low_risk_count', 0)
        
        findings = []
        
        if flagged > 0:
            findings.append(ListItem(Paragraph(
                f"<b>{flagged}</b> processes were flagged for suspicious behavior",
                self.styles['CustomBody']
            )))
        
        if high_risk > 0:
            findings.append(ListItem(Paragraph(
                f"<font color='#e63946'><b>{high_risk}</b> high-risk processes</font> require immediate attention",
                self.styles['CustomBody']
            )))
        
        if medium_risk > 0:
            findings.append(ListItem(Paragraph(
                f"<font color='#f4a261'><b>{medium_risk}</b> medium-risk processes</font> warrant investigation",
                self.styles['CustomBody']
            )))
        
        if low_risk > 0:
            findings.append(ListItem(Paragraph(
                f"<b>{low_risk}</b> processes were classified as low risk",
                self.styles['CustomBody']
            )))
        
        if not findings:
            findings.append(ListItem(Paragraph(
                "No significant threats were detected in this analysis",
                self.styles['CustomBody']
            )))
        
        elements.append(ListFlowable(
            findings,
            bulletType='bullet',
            bulletFontSize=8,
            leftIndent=20,
        ))
        
        elements.append(Spacer(1, 0.2 * inch))
        
        # Detection methods
        elements.append(Paragraph("Detection Methods Applied", self.styles['Subsection']))
        
        methods = [
            ListItem(Paragraph("LOLBAS (Living Off The Land Binaries and Scripts) detection", self.styles['CustomBody'])),
            ListItem(Paragraph("Suspicious path pattern matching (temp folders, unusual locations)", self.styles['CustomBody'])),
            ListItem(Paragraph("Parent-child process relationship analysis", self.styles['CustomBody'])),
            ListItem(Paragraph("Registry persistence mechanism detection", self.styles['CustomBody'])),
        ]
        
        elements.append(ListFlowable(
            methods,
            bulletType='bullet',
            bulletFontSize=8,
            leftIndent=20,
        ))
        
        return elements
    
    def _create_risk_distribution(self, result: dict) -> list:
        """Create risk distribution visualization."""
        elements = []
        
        elements.append(Paragraph("Risk Distribution", self.styles['SectionHeader']))
        
        high_risk = result.get('high_risk_count', 0)
        medium_risk = result.get('medium_risk_count', 0)
        low_risk = result.get('low_risk_count', 0)
        total = high_risk + medium_risk + low_risk
        
        if total == 0:
            elements.append(Paragraph(
                "No processes were analyzed for risk distribution.",
                self.styles['CustomBody']
            ))
            return elements
        
        # Create pie chart
        drawing = Drawing(400, 200)
        
        pie = Pie()
        pie.x = 100
        pie.y = 25
        pie.width = 150
        pie.height = 150
        pie.data = [high_risk, medium_risk, low_risk]
        pie.labels = [f'High ({high_risk})', f'Medium ({medium_risk})', f'Low ({low_risk})']
        pie.slices.strokeWidth = 0.5
        pie.slices[0].fillColor = colors.HexColor('#e63946')
        pie.slices[1].fillColor = colors.HexColor('#f4a261')
        pie.slices[2].fillColor = colors.HexColor('#2a9d8f')
        
        # Only show slices with values
        for i, val in enumerate([high_risk, medium_risk, low_risk]):
            if val == 0:
                pie.slices[i].visible = False
        
        drawing.add(pie)
        
        # Add legend
        legend_y = 170
        legend_x = 300
        
        for i, (label, color) in enumerate([
            (f'High Risk: {high_risk}', '#e63946'),
            (f'Medium Risk: {medium_risk}', '#f4a261'),
            (f'Low Risk: {low_risk}', '#2a9d8f'),
        ]):
            rect = Rect(legend_x, legend_y - (i * 25), 15, 15)
            rect.fillColor = colors.HexColor(color)
            rect.strokeColor = colors.black
            drawing.add(rect)
            
            text = String(legend_x + 20, legend_y - (i * 25) + 3, label)
            text.fontSize = 10
            drawing.add(text)
        
        elements.append(drawing)
        elements.append(Spacer(1, 0.3 * inch))
        
        # Risk percentage breakdown
        elements.append(Paragraph("Risk Breakdown", self.styles['Subsection']))
        
        data = [
            ['Risk Level', 'Count', 'Percentage'],
            ['High Risk', str(high_risk), f'{(high_risk/total*100):.1f}%'],
            ['Medium Risk', str(medium_risk), f'{(medium_risk/total*100):.1f}%'],
            ['Low Risk', str(low_risk), f'{(low_risk/total*100):.1f}%'],
            ['Total', str(total), '100%'],
        ]
        
        table = Table(data, colWidths=[2 * inch, 1.5 * inch, 1.5 * inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#16213e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cccccc')),
            # Row colors
            ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#ffe6e6')),
            ('BACKGROUND', (0, 2), (-1, 2), colors.HexColor('#fff3e0')),
            ('BACKGROUND', (0, 3), (-1, 3), colors.HexColor('#e8f5e9')),
            ('BACKGROUND', (0, 4), (-1, 4), colors.HexColor('#f0f0f0')),
            ('FONTNAME', (0, 4), (-1, 4), 'Helvetica-Bold'),
        ]))
        
        elements.append(table)
        
        return elements
    
    def _create_top_threats(self, result: dict) -> list:
        """Create top threats section."""
        elements = []
        
        elements.append(Paragraph("Top Threats", self.styles['SectionHeader']))
        
        top_threats = result.get('top_threats', [])
        
        if not top_threats:
            elements.append(Paragraph(
                "No significant threats were identified in this analysis.",
                self.styles['CustomBody']
            ))
            return elements
        
        elements.append(Paragraph(
            f"The following {len(top_threats)} processes were identified as potentially suspicious:",
            self.styles['CustomBody']
        ))
        
        elements.append(Spacer(1, 0.2 * inch))
        
        # Create threats table
        data = [['Process Name', 'PID', 'Risk Score', 'Legitimacy', 'Matched Rules']]
        
        for threat in top_threats[:10]:  # Limit to top 10
            process_name = threat.get('process_name', 'Unknown')
            if len(process_name) > 30:
                process_name = process_name[:27] + '...'
            
            pid = str(threat.get('pid', 'N/A'))
            risk_score = str(threat.get('risk_score', 0))
            legitimacy = threat.get('legitimacy', 'unknown')
            
            rules = threat.get('matched_rules', [])
            rules_str = ', '.join(rules[:2]) if rules else 'None'
            if len(rules) > 2:
                rules_str += f' (+{len(rules)-2} more)'
            
            data.append([process_name, pid, risk_score, legitimacy, rules_str])
        
        # Calculate column widths
        col_widths = [2 * inch, 0.7 * inch, 0.8 * inch, 0.9 * inch, 2.2 * inch]
        
        table = Table(data, colWidths=col_widths)
        
        style = [
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#16213e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 0), (2, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cccccc')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]
        
        # Add row-specific styling based on risk level
        for i, threat in enumerate(top_threats[:10], start=1):
            risk_score = threat.get('risk_score', 0)
            legitimacy = threat.get('legitimacy', 'unknown')
            
            if risk_score >= 50 or legitimacy == 'malicious':
                style.append(('BACKGROUND', (0, i), (-1, i), colors.HexColor('#ffe6e6')))
            elif risk_score >= 20 or legitimacy == 'suspicious':
                style.append(('BACKGROUND', (0, i), (-1, i), colors.HexColor('#fff3e0')))
            else:
                style.append(('BACKGROUND', (0, i), (-1, i), colors.HexColor('#f9f9f9')))
        
        table.setStyle(TableStyle(style))
        elements.append(table)
        
        return elements
    
    def _create_detailed_findings(self, result: dict) -> list:
        """Create detailed findings for top threats."""
        elements = []
        
        elements.append(Paragraph("Detailed Findings", self.styles['SectionHeader']))
        
        top_threats = result.get('top_threats', [])
        
        if not top_threats:
            elements.append(Paragraph(
                "No detailed findings to report.",
                self.styles['CustomBody']
            ))
            return elements
        
        # Show details for top 5 threats
        for i, threat in enumerate(top_threats[:5], start=1):
            process_name = threat.get('process_name', 'Unknown')
            pid = threat.get('pid', 'N/A')
            image_path = threat.get('image_path', 'Unknown')
            risk_score = threat.get('risk_score', 0)
            legitimacy = threat.get('legitimacy', 'unknown')
            behavior_tags = threat.get('behavior_tags', [])
            matched_rules = threat.get('matched_rules', [])
            ai_reasoning = threat.get('ai_reasoning')
            
            # Risk level styling
            if risk_score >= 50:
                risk_style = self.styles['HighRisk']
                risk_label = "HIGH RISK"
            elif risk_score >= 20:
                risk_style = self.styles['MediumRisk']
                risk_label = "MEDIUM RISK"
            else:
                risk_style = self.styles['LowRisk']
                risk_label = "LOW RISK"
            
            # Process header
            elements.append(Paragraph(
                f"Finding #{i}: {process_name} (PID: {pid})",
                self.styles['Subsection']
            ))
            
            elements.append(Paragraph(
                f"<b>{risk_label}</b> - Score: {risk_score}",
                risk_style
            ))
            
            elements.append(Spacer(1, 0.1 * inch))
            
            # Process details table
            details_data = [
                ['Property', 'Value'],
                ['Image Path', image_path if len(image_path) < 60 else image_path[:57] + '...'],
                ['Legitimacy', legitimacy.upper()],
                ['Risk Score', str(risk_score)],
            ]
            
            if behavior_tags:
                details_data.append(['Behavior Tags', ', '.join(behavior_tags)])
            
            details_table = Table(details_data, colWidths=[1.5 * inch, 5.1 * inch])
            details_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e8e8e8')),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
                ('TOPPADDING', (0, 0), (-1, -1), 5),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cccccc')),
            ]))
            
            elements.append(details_table)
            elements.append(Spacer(1, 0.15 * inch))
            
            # Matched rules
            if matched_rules:
                elements.append(Paragraph("<b>Matched Detection Rules:</b>", self.styles['CustomBody']))
                
                rules_list = [
                    ListItem(Paragraph(rule, self.styles['CustomBody']))
                    for rule in matched_rules
                ]
                
                elements.append(ListFlowable(
                    rules_list,
                    bulletType='bullet',
                    bulletFontSize=6,
                    leftIndent=15,
                ))
            
            elements.append(Spacer(1, 0.1 * inch))
            
            # AI reasoning if available
            if ai_reasoning:
                elements.append(Paragraph("<b>AI Analysis:</b>", self.styles['CustomBody']))
                
                # Wrap AI reasoning in a styled box
                ai_text = ai_reasoning.replace('\n', '<br/>')
                elements.append(Paragraph(
                    f"<i>{ai_text}</i>",
                    ParagraphStyle(
                        name='AIReasoning',
                        parent=self.styles['CustomBody'],
                        fontSize=9,
                        leftIndent=10,
                        rightIndent=10,
                        backColor=colors.HexColor('#f5f5f5'),
                        borderPadding=8,
                    )
                ))
            
            elements.append(Spacer(1, 0.3 * inch))
        
        return elements
    
    def _add_header_footer(self, canvas, doc) -> None:
        """Add header and footer to each page."""
        canvas.saveState()
        
        # Footer
        footer_text = f"ProcBench Analysis Report - Page {doc.page}"
        canvas.setFont('Helvetica', 8)
        canvas.setFillColor(colors.HexColor('#666666'))
        canvas.drawString(0.75 * inch, 0.5 * inch, footer_text)
        
        # Right side footer with timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d")
        canvas.drawRightString(
            self.page_size[0] - 0.75 * inch,
            0.5 * inch,
            f"Generated: {timestamp}"
        )
        
        canvas.restoreState()
