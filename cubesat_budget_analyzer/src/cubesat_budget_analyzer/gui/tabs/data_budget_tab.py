"""Data Budget Analysis tab for CubeSat Budget Analyzer."""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
                           QDoubleSpinBox, QMessageBox, QFileDialog,
                           QGroupBox, QPushButton, QLabel)
from PyQt6.QtCore import Qt
import math

class ParameterGroup(QGroupBox):
    """Custom group box for parameters."""
    
    def __init__(self, title, parent=None):
        super().__init__(title, parent)
        self.setStyleSheet("""
            QGroupBox {
                font-size: 14px;
                font-weight: bold;
                border: 2px solid #3d3d3d;
                border-radius: 8px;
                margin-top: 1em;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)

class DataBudgetTab(QWidget):
    """Tab for Data Budget Analysis calculations."""
    
    # Constants
    BYTES_PER_MB = 1024 * 1024
    SECONDS_PER_MINUTE = 60
    SECONDS_PER_DAY = 86400
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface."""
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        self.setLayout(main_layout)
        
        # Parameters and Results sections
        top_section = QHBoxLayout()
        params_widget = self.create_parameters_section()
        results_group = self.create_results_section()
        
        top_section.addWidget(params_widget, stretch=2)
        top_section.addWidget(results_group, stretch=1)
        main_layout.addLayout(top_section)
        
        # Buttons section
        main_layout.addStretch()
        main_layout.addWidget(self.create_buttons_section(), alignment=Qt.AlignmentFlag.AlignCenter)
    
    def create_parameters_section(self):
        """Create the parameters input section."""
        params_widget = QWidget()
        params_layout = QVBoxLayout(params_widget)
        params_layout.setSpacing(15)
        params_layout.setContentsMargins(0, 0, 0, 0)
        
        # Data Generation Parameters
        generation_group = ParameterGroup("Data Generation Parameters")
        generation_layout = QFormLayout()
        
        self.payload_rate = self.create_spin_box(0.001, 1000, 1.0, " Mbps",
            "Data generation rate from payload instruments")
        generation_layout.addRow("Payload Data Rate:", self.payload_rate)
        
        generation_group.setLayout(generation_layout)
        params_layout.addWidget(generation_group)
        
        # Storage Parameters
        storage_group = ParameterGroup("Storage Parameters")
        storage_layout = QFormLayout()
        
        self.storage_capacity = self.create_spin_box(1, 1000, 32, " GB",
            "Total onboard storage capacity")
        storage_layout.addRow("Storage Capacity:", self.storage_capacity)
        
        storage_group.setLayout(storage_layout)
        params_layout.addWidget(storage_group)
        
        # Transmission Parameters
        transmission_group = ParameterGroup("Transmission Parameters")
        transmission_layout = QFormLayout()
        
        self.downlink_rate = self.create_spin_box(0.001, 1000, 9.6, " Mbps",
            "Data transmission rate to ground station")
        self.pass_duration = self.create_spin_box(1, 60, 10, " min",
            "Duration of each ground station pass")
        self.passes_per_day = self.create_spin_box(1, 24, 4, " passes",
            "Number of ground station passes per day")
        
        transmission_layout.addRow("Downlink Rate:", self.downlink_rate)
        transmission_layout.addRow("Pass Duration:", self.pass_duration)
        transmission_layout.addRow("Passes per Day:", self.passes_per_day)
        
        transmission_group.setLayout(transmission_layout)
        params_layout.addWidget(transmission_group)
        
        return params_widget
    
    def create_results_section(self):
        """Create the results display section."""
        results_group = ParameterGroup("Data Budget Results")
        results_layout = QVBoxLayout()
        results_layout.setSpacing(20)
        results_layout.setContentsMargins(20, 20, 20, 20)
        
        self.results_widget = QWidget()
        self.results_layout = QFormLayout(self.results_widget)
        self.results_layout.setSpacing(15)
        results_layout.addWidget(self.results_widget)
        results_layout.addStretch()
        results_group.setLayout(results_layout)
        
        return results_group
    
    def create_buttons_section(self):
        """Create the buttons section."""
        buttons_widget = QWidget()
        buttons_layout = QHBoxLayout(buttons_widget)
        buttons_layout.setSpacing(20)
        
        calc_button = QPushButton("Calculate Data Budget")
        calc_button.setMinimumSize(200, 50)
        calc_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #45a049; }
            QPushButton:pressed { background-color: #3d8b40; }
        """)
        calc_button.clicked.connect(self.calculate_data_budget)
        
        report_button = QPushButton("Generate PDF Report")
        report_button.setMinimumSize(200, 50)
        report_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #1976D2; }
            QPushButton:pressed { background-color: #1565C0; }
        """)
        report_button.clicked.connect(self.generate_report)
        
        back_button = QPushButton("← Back")
        back_button.setFixedSize(120, 50)
        back_button.setStyleSheet("""
            QPushButton {
                background-color: #666;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 13px;
            }
            QPushButton:hover { background-color: #555; }
            QPushButton:pressed { background-color: #444; }
        """)
        if self.parent:
            back_button.clicked.connect(self.parent.show_home_page)
        
        buttons_layout.addWidget(calc_button)
        buttons_layout.addWidget(report_button)
        buttons_layout.addWidget(back_button)
        
        return buttons_widget
    
    def create_spin_box(self, min_val, max_val, default_val, suffix, tooltip):
        """Create a styled spin box."""
        spin_box = QDoubleSpinBox()
        spin_box.setRange(min_val, max_val)
        spin_box.setValue(default_val)
        spin_box.setSuffix(suffix)
        spin_box.setToolTip(tooltip)
        spin_box.setStyleSheet("""
            QDoubleSpinBox {
                padding: 5px;
                border: 1px solid #555;
                border-radius: 4px;
                background: #2d2d2d;
                min-width: 100px;
            }
            QDoubleSpinBox:hover { border-color: #666; }
            QDoubleSpinBox:focus { border-color: #2196F3; }
        """)
        return spin_box
    
    def calculate_data_budget(self):
        """Calculate the data budget using actual input parameters."""
        # Calculate daily data generation
        daily_data_gen = self.payload_rate.value() * self.SECONDS_PER_DAY  # MB per day
        
        # Calculate daily data transmission capacity
        transmission_time = (self.pass_duration.value() * self.SECONDS_PER_MINUTE * 
                           self.passes_per_day.value())  # seconds per day
        daily_transmission = self.downlink_rate.value() * transmission_time  # MB per day
        
        # Calculate storage requirements and margins
        storage_capacity_mb = self.storage_capacity.value() * 1024  # Convert GB to MB
        storage_margin = storage_capacity_mb - daily_data_gen
        transmission_margin = daily_transmission - daily_data_gen
        
        # Display results
        self.display_results([
            ("Daily Data Generation", f"{daily_data_gen:.1f} MB/day"),
            ("Daily Transmission Capacity", f"{daily_transmission:.1f} MB/day"),
            ("Storage Utilization", f"{(daily_data_gen/storage_capacity_mb)*100:.1f}%"),
            ("Storage Margin", f"{storage_margin:.1f} MB"),
            ("Transmission Margin", f"{transmission_margin:.1f} MB/day")
        ])
        
        # Show warnings if needed
        if storage_margin < 0:
            QMessageBox.warning(self, "Storage Warning",
                              f"Warning: Storage capacity insufficient by {abs(storage_margin):.1f} MB/day")
        elif transmission_margin < 0:
            QMessageBox.warning(self, "Transmission Warning",
                              f"Warning: Cannot downlink all daily data. Deficit: {abs(transmission_margin):.1f} MB/day")
    
    def display_results(self, results):
        """Display the calculation results."""
        # Clear previous results
        while self.results_layout.count():
            item = self.results_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Add new results
        for label_text, value in results:
            container = QWidget()
            container.setStyleSheet("QWidget { background-color: #1e1e1e; border-radius: 4px; }")
            
            layout = QVBoxLayout(container)
            layout.setContentsMargins(10, 10, 10, 10)
            
            label = QLabel(label_text)
            label.setStyleSheet("QLabel { color: #a0a0a0; font-size: 13px; }")
            layout.addWidget(label)
            
            value_label = QLabel(value)
            value_label.setStyleSheet("""
                QLabel {
                    color: #4CAF50;
                    font-size: 20px;
                    font-weight: bold;
                }
            """)
            layout.addWidget(value_label)
            
            self.results_layout.addRow(container)
    
    def generate_report(self):
        """Generate a PDF report of the data budget analysis."""
        filename, _ = QFileDialog.getSaveFileName(self, "Save PDF Report", "", "PDF Files (*.pdf)")
        if not filename:
            return
            
        if not filename.lower().endswith('.pdf'):
            filename += '.pdf'
            
        try:
            # Import required reportlab modules
            from reportlab.lib import colors
            from reportlab.lib.pagesizes import letter
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
            
            # Create the PDF document
            doc = SimpleDocTemplate(filename, pagesize=letter)
            styles = getSampleStyleSheet()
            
            # Prepare content list
            content = []
            
            # Add title
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                spaceAfter=30,
                alignment=1  # Center alignment
            )
            content.append(Paragraph("Data Budget Analysis Report", title_style))
            content.append(Spacer(1, 20))
            
            # Collect parameters
            params = {
                "Data Generation Parameters": {
                    "Payload Data Rate": f"{self.payload_rate.value()} Mbps"
                },
                "Storage Parameters": {
                    "Storage Capacity": f"{self.storage_capacity.value()} GB"
                },
                "Transmission Parameters": {
                    "Downlink Rate": f"{self.downlink_rate.value()} Mbps",
                    "Pass Duration": f"{self.pass_duration.value()} min",
                    "Passes per Day": f"{self.passes_per_day.value()} passes"
                }
            }
            
            # Add parameters tables
            for section, section_params in params.items():
                content.append(Paragraph(section, styles['Heading2']))
                content.append(Spacer(1, 10))
                
                data = [["Parameter", "Value"]]
                for param, value in section_params.items():
                    data.append([param, value])
                
                table = Table(data, colWidths=[250, 200])
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#333333')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f5f5f5')),
                    ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 1), (-1, -1), 10),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('PADDING', (0, 0), (-1, -1), 6),
                ]))
                content.append(table)
                content.append(Spacer(1, 20))
            
            # Add Results section
            content.append(Paragraph("Calculation Results", styles['Heading2']))
            content.append(Spacer(1, 10))
            
            # Get current results
            results = []
            for i in range(self.results_layout.count()):
                container = self.results_layout.itemAt(i).widget()
                if container:
                    label = container.layout().itemAt(0).widget().text()
                    value = container.layout().itemAt(1).widget().text()
                    results.append([label, value])
            
            # Create results table
            if results:
                data = [["Parameter", "Value"]]
                data.extend(results)
                
                table = Table(data, colWidths=[250, 200])
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#333333')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f5f5f5')),
                    ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 1), (-1, -1), 10),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('PADDING', (0, 0), (-1, -1), 6),
                ]))
                content.append(table)
            else:
                content.append(Paragraph("No results available. Please calculate the data budget first.",
                                      styles['Normal']))
            
            # Build the PDF
            doc.build(content)
            
            QMessageBox.information(self, "Success",
                                  f"PDF report has been generated and saved to:\n{filename}")
            
        except ImportError:
            QMessageBox.critical(self, "Error",
                               "Could not generate PDF. Please install reportlab package.")
        except Exception as e:
            QMessageBox.critical(self, "Error",
                               f"Failed to generate PDF report: {str(e)}") 