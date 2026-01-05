from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.pdfgen import canvas
import os
from typing import Dict, Any
import matplotlib.pyplot as plt
import io
from datetime import datetime

class ReportGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()

    def _setup_custom_styles(self):
        """Set up custom paragraph styles for the report."""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            textColor=colors.HexColor('#1DCD9F')
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceAfter=12,
            textColor=colors.HexColor('#169976')
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceAfter=6
        ))
        
        self.styles.add(ParagraphStyle(
            name='Warning',
            parent=self.styles['Normal'],
            fontSize=12,
            textColor=colors.HexColor('#1DCD9F'),
            spaceAfter=6
        ))

    def generate_link_budget_report(self, data: dict):
        """Generate a PDF report for link budget analysis."""
        # Create output directory if it doesn't exist
        output_dir = os.path.join(os.getcwd(), 'reports')
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = os.path.join(output_dir, f'link_budget_report_{timestamp}.pdf')
        
        # Create PDF document
        doc = SimpleDocTemplate(
            filename,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        # Build content
        story = []
        
        # Title
        story.append(Paragraph(
            "Link Budget Analysis Report",
            self.styles['CustomTitle']
        ))
        story.append(Spacer(1, 12))
        
        # Timestamp
        story.append(Paragraph(
            f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            self.styles['CustomBody']
        ))
        story.append(Spacer(1, 20))
        
        # Input Parameters
        story.append(Paragraph("Input Parameters", self.styles['CustomHeading']))
        story.append(Spacer(1, 12))
        
        inputs = data['inputs']
        input_data = [
            ["Parameter", "Value"],
            ["Transmit Power", f"{inputs['tx_power_dbm']} dBm"],
            ["Transmitter Gain", f"{inputs['tx_gain_dbi']} dBi"],
            ["Receiver Gain", f"{inputs['rx_gain_dbi']} dBi"],
            ["Carrier Frequency", f"{inputs['freq_ghz']} GHz"],
            ["Distance", f"{inputs['distance_km']} km"],
            ["Path Loss", f"{inputs['path_loss_db']} dB"],
            ["Atmospheric Loss", f"{inputs['atm_loss_db']} dB"],
            ["System Temperature", f"{inputs['sys_temp_k']} K"],
            ["Bandwidth", f"{inputs['bandwidth_hz']} Hz"],
            ["Modulation Scheme", inputs['modulation']],
            ["Propagation Model", inputs['propagation']],
            ["Required Eb/N0", f"{inputs['required_ebn0_db']} dB"]
        ]
        
        table = Table(input_data, colWidths=[3*inch, 2*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#222222')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(table)
        story.append(Spacer(1, 20))
        
        # Results
        story.append(Paragraph("Analysis Results", self.styles['CustomHeading']))
        story.append(Spacer(1, 12))
        
        results = data['results']
        if results:
            results_data = [
                ["Metric", "Value"],
                ["Received Power", f"{results['received_power_dbm']} dBm"],
                ["Carrier-to-Noise Ratio", f"{results['cnr_db']} dB"],
                ["Bit Error Rate", f"{results['ber']:.2e}"],
                ["Link Margin", f"{results['link_margin_db']} dB"]
            ]
            
            table = Table(results_data, colWidths=[3*inch, 2*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#222222')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(table)
            story.append(Spacer(1, 20))
            
            # Warnings
            if results.get('warnings'):
                story.append(Paragraph("Warnings", self.styles['CustomHeading']))
                story.append(Spacer(1, 12))
                story.append(Paragraph(results['warnings'], self.styles['Warning']))
        else:
            story.append(Paragraph(
                "No results available. Please run the analysis first.",
                self.styles['CustomBody']
            ))
        
        # Build PDF
        doc.build(story)
        return filename

    def generate_pdf(self, data: Dict[str, Any], output_path: str):
        """Generate a PDF report from the analysis data."""
        doc = SimpleDocTemplate(output_path, pagesize=letter)
        story = []

        # Title
        title = "CubeSat Budget Analysis Report"
        story.append(Paragraph(title, self.styles['CustomTitle']))
        
        # Metadata
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        story.append(Paragraph(f"Generated: {timestamp}", self.styles['Normal']))
        story.append(Spacer(1, 20))

        # Link Budget Section
        if 'link_budget' in data:
            story.append(Paragraph("Link Budget Analysis", self.styles['CustomHeading']))
            link_data = data['link_budget']
            
            # Create link budget table
            link_table_data = [
                ["Parameter", "Value"],
                ["Received Power", f"{link_data['received_power_dbm']:.2f} dBm"],
                ["Carrier-to-Noise Ratio", f"{link_data['cnr_db']:.2f} dB"],
                ["Bit Error Rate", f"{link_data['ber']:.2e}"],
                ["Link Margin", f"{link_data['link_margin_db']:.2f} dB"]
            ]
            
            table = Table(link_table_data, colWidths=[200, 200])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 14),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(table)
            story.append(Spacer(1, 20))

        # Data Budget Section
        if 'data_budget' in data:
            story.append(Paragraph("Data Budget Analysis", self.styles['CustomHeading']))
            data_budget = data['data_budget']
            
            # Create data budget table
            data_table_data = [
                ["Parameter", "Value"],
                ["Daily Data Generated", f"{data_budget['daily_data_gb']:.2f} GB/day"],
                ["Daily Downlink Capacity", f"{data_budget['daily_downlink_capacity_gb']:.2f} GB/day"],
                ["Storage Usage", f"{data_budget['storage_usage_gb']:.2f} GB"],
                ["Expected Backlog", f"{data_budget['backlog_gb']:.2f} GB/day"]
            ]
            
            if data_budget.get('days_until_full') is not None:
                data_table_data.append(
                    ["Days Until Storage Full", f"{data_budget['days_until_full']:.1f} days"]
                )
            
            table = Table(data_table_data, colWidths=[200, 200])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 14),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(table)

        # Build the PDF
        doc.build(story) 