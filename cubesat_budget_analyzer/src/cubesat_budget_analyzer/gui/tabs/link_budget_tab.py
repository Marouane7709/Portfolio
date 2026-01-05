"""Link Budget Analysis tab for SatAnalytica."""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
                           QLabel, QPushButton, QGroupBox, QComboBox,
                           QDoubleSpinBox, QMessageBox, QFileDialog)
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

class LinkBudgetTab(QWidget):
    """Tab for Link Budget Analysis calculations."""
    
    # Constants
    BOLTZMANN = 1.38e-23  # Boltzmann's constant
    SPEED_OF_LIGHT = 3e8  # Speed of light in m/s
    DEFAULT_ORBIT_HEIGHT = 500000  # Default LEO satellite height in meters
    
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
        
        # Transmitter Parameters
        tx_group = ParameterGroup("Transmitter Parameters")
        tx_layout = QFormLayout()
        tx_layout.setSpacing(10)
        
        # Power input with unit selection
        tx_power_widget = QWidget()
        tx_power_layout = QHBoxLayout(tx_power_widget)
        tx_power_layout.setContentsMargins(0, 0, 0, 0)
        
        self.tx_power = self.create_spin_box(-50, 50, 1.0, " W", "Transmitter output power")
        self.tx_power_unit = self.create_combo_box(["W", "dBm"], "Select power unit")
        self.tx_power_unit.currentTextChanged.connect(self.on_power_unit_changed)
        
        tx_power_layout.addWidget(self.tx_power)
        tx_power_layout.addWidget(self.tx_power_unit)
        tx_layout.addRow("Transmit Power:", tx_power_widget)
        
        self.tx_gain = self.create_spin_box(-20, 50, 0, " dBi", "Transmitter antenna gain")
        tx_layout.addRow("Transmitter Gain:", self.tx_gain)
        tx_group.setLayout(tx_layout)
        params_layout.addWidget(tx_group)
        
        # Channel Parameters
        channel_group = ParameterGroup("Channel Parameters")
        channel_layout = QFormLayout()
        
        # Frequency input with unit selection
        freq_widget = QWidget()
        freq_layout = QHBoxLayout(freq_widget)
        freq_layout.setContentsMargins(0, 0, 0, 0)
        
        self.freq_value = self.create_spin_box(0, 100000, 2.4, " MHz", "Operating frequency")
        self.freq_unit = self.create_combo_box(["MHz", "GHz"], "Select frequency unit")
        self.freq_unit.currentTextChanged.connect(self.on_freq_unit_changed)
        
        freq_layout.addWidget(self.freq_value)
        freq_layout.addWidget(self.freq_unit)
        channel_layout.addRow("Operating Frequency:", freq_widget)
        
        self.fspl = self.create_spin_box(0, 200, 0, " dB", "Free space path loss")
        self.atm_loss = self.create_spin_box(-50, 0, -0.5, " dB", "Atmospheric loss")
        self.prop_model = self.create_combo_box(["AWGN"], "Select propagation model")
        
        channel_layout.addRow("Free Space Path Loss:", self.fspl)
        channel_layout.addRow("Atmospheric Loss:", self.atm_loss)
        channel_layout.addRow("Propagation Model:", self.prop_model)
        channel_group.setLayout(channel_layout)
        params_layout.addWidget(channel_group)
        
        # Receiver Parameters
        rx_group = ParameterGroup("Receiver Parameters")
        rx_layout = QFormLayout()
        
        self.rx_gain = self.create_spin_box(-20, 50, 0, " dBi", "Receiver antenna gain")
        self.sys_temp = self.create_spin_box(50, 500, 290, " K", "System noise temperature")
        self.bandwidth = self.create_spin_box(1e3, 1e9, 1e6, " Hz", "Channel bandwidth")
        self.required_ebn0 = self.create_spin_box(0, 30, 10, " dB", "Required Eb/N0")
        
        rx_layout.addRow("Receiver Gain:", self.rx_gain)
        rx_layout.addRow("System Temperature:", self.sys_temp)
        rx_layout.addRow("Bandwidth:", self.bandwidth)
        rx_layout.addRow("Required Eb/N0:", self.required_ebn0)
        rx_group.setLayout(rx_layout)
        params_layout.addWidget(rx_group)
        
        return params_widget
    
    def create_results_section(self):
        """Create the results display section."""
        results_group = ParameterGroup("Link Budget Results")
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
        
        calc_button = QPushButton("Calculate Link Budget")
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
        calc_button.clicked.connect(self.calculate_link_budget)
        
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
    
    def create_combo_box(self, items, tooltip):
        """Create a styled combo box."""
        combo = QComboBox()
        combo.addItems(items)
        combo.setToolTip(tooltip)
        combo.setStyleSheet("""
            QComboBox {
                padding: 5px;
                border: 1px solid #555;
                border-radius: 4px;
                background: #2d2d2d;
                min-width: 100px;
            }
            QComboBox:hover { border-color: #666; }
            QComboBox:focus { border-color: #2196F3; }
            QComboBox::drop-down { border: none; }
            QComboBox::down-arrow { image: none; }
        """)
        return combo
    
    def calculate_link_budget(self):
        """Calculate the link budget using actual input parameters."""
        # Convert power to dBW
        tx_power_val = self.tx_power.value()
        tx_power_dbw = (10 * math.log10(tx_power_val) if self.tx_power_unit.currentText() == "W" 
                       else tx_power_val - 30)
        
        # Calculate EIRP
        eirp = tx_power_dbw + self.tx_gain.value()
        
        # Calculate path loss
        freq_hz = self.get_frequency_hz()
        fspl = (self.calculate_fspl(freq_hz) if self.fspl.value() == 0 
               else self.fspl.value())
        total_path_loss = fspl + self.atm_loss.value()
        
        # Calculate received power and noise
        received_power = eirp - total_path_loss + self.rx_gain.value()
        noise_factor = 10 * math.log10(self.BOLTZMANN * self.sys_temp.value())
        
        # Calculate C/N0 and Eb/N0
        cn0 = received_power - noise_factor
        ebn0 = cn0 - 10 * math.log10(self.bandwidth.value())
        link_margin = ebn0 - self.required_ebn0.value()
        
        # Display results
        self.display_results([
            ("EIRP", f"{eirp:.1f} dBW"),
            ("Path Loss", f"{total_path_loss:.1f} dB"),
            ("Received Power", f"{received_power:.1f} dBW"),
            ("C/N0", f"{cn0:.1f} dB-Hz"),
            ("Link Margin", f"{link_margin:.1f} dB")
        ])
        
        # Show warnings if needed
        if link_margin < 0:
            QMessageBox.warning(self, "Link Margin Warning",
                              f"Warning: Negative link margin ({link_margin:.1f} dB)")
        elif link_margin < 3:
            QMessageBox.warning(self, "Link Margin Caution",
                              f"Caution: Low link margin ({link_margin:.1f} dB)")
    
    def calculate_fspl(self, freq_hz):
        """Calculate Free Space Path Loss."""
        return (20 * math.log10(self.DEFAULT_ORBIT_HEIGHT) + 
                20 * math.log10(freq_hz) + 
                20 * math.log10(4 * math.pi / self.SPEED_OF_LIGHT))
    
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
    
    def get_frequency_hz(self):
        """Convert frequency to Hz based on selected unit."""
        value = self.freq_value.value()
        return value * 1e9 if self.freq_unit.currentText() == "GHz" else value * 1e6
    
    def on_power_unit_changed(self, unit):
        """Handle power unit change between W and dBm."""
        current_value = self.tx_power.value()
        if unit == "W" and self.tx_power.suffix() == " dBm":
            self.tx_power.setValue(10 ** ((current_value - 30) / 10))
        elif unit == "dBm" and self.tx_power.suffix() == " W":
            self.tx_power.setValue(10 * math.log10(current_value * 1000))
        self.tx_power.setSuffix(f" {unit}")
    
    def on_freq_unit_changed(self, unit):
        """Handle frequency unit change between MHz and GHz."""
        current_value = self.freq_value.value()
        if unit == "GHz" and self.freq_value.suffix() == " MHz":
            self.freq_value.setValue(current_value / 1000)
        elif unit == "MHz" and self.freq_value.suffix() == " GHz":
            self.freq_value.setValue(current_value * 1000)
        self.freq_value.setSuffix(f" {unit}")
    
    def generate_report(self):
        """Generate a PDF report of the link budget analysis."""
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
            content.append(Paragraph("Link Budget Analysis Report", title_style))
            content.append(Spacer(1, 20))
            
            # Collect parameters
            params = {
                "Transmitter Parameters": {
                    "Transmit Power": f"{self.tx_power.value()} {self.tx_power_unit.currentText()}",
                    "Transmitter Gain": f"{self.tx_gain.value()} dBi"
                },
                "Channel Parameters": {
                    "Operating Frequency": f"{self.freq_value.value()} {self.freq_unit.currentText()}",
                    "Free Space Path Loss": f"{self.fspl.value()} dB",
                    "Atmospheric Loss": f"{self.atm_loss.value()} dB",
                    "Propagation Model": self.prop_model.currentText()
                },
                "Receiver Parameters": {
                    "Receiver Gain": f"{self.rx_gain.value()} dBi",
                    "System Temperature": f"{self.sys_temp.value()} K",
                    "Bandwidth": f"{self.bandwidth.value()} Hz",
                    "Required Eb/N0": f"{self.required_ebn0.value()} dB"
                }
            }
            
            # Add parameters tables
            for section, section_params in params.items():
                # Add section header
                content.append(Paragraph(section, styles['Heading2']))
                content.append(Spacer(1, 10))
                
                # Create table data
                data = [["Parameter", "Value"]]  # Header row
                for param, value in section_params.items():
                    data.append([param, value])
                
                # Create and style the table
                table = Table(data, colWidths=[250, 200])
                table.setStyle(TableStyle([
                    # Header row styling
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#333333')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    # Data rows styling
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
                data = [["Parameter", "Value"]]  # Header row
                data.extend(results)
                
                table = Table(data, colWidths=[250, 200])
                table.setStyle(TableStyle([
                    # Header row styling
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#333333')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    # Data rows styling
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
                content.append(Paragraph("No results available. Please calculate the link budget first.", 
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