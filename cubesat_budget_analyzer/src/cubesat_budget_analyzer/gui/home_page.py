"""Home page for SatAnalytica."""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                           QPushButton, QSpacerItem, QSizePolicy, QFrame,
                           QGridLayout, QMessageBox)
from PyQt6.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QFont, QIcon, QPixmap

class AnalysisButton(QPushButton):
    """Custom button for analysis options."""
    
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.setup_ui(title)
    
    def setup_ui(self, title):
        """Setup the button's UI."""
        self.setText(title)
        self.setMinimumSize(250, 55)
        self.setStyleSheet("""
            AnalysisButton {
                background-color: #2d2d2d;
                border: 2px solid #444;
                border-radius: 10px;
                padding: 15px;
                color: white;
                font-size: 16px;
                font-weight: bold;
                font-family: 'Segoe UI', 'Roboto', sans-serif;
            }
            AnalysisButton:hover {
                background-color: #3d3d3d;
                border-color: #4CAF50;
            }
            AnalysisButton:pressed {
                background-color: #262626;
            }
        """)

class HomePage(QWidget):
    """Home page widget."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface."""
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(30)
        self.setLayout(main_layout)
        
        # Welcome message
        welcome_label = QLabel("Welcome, Engineer!")
        welcome_label.setObjectName("welcomeTitle")
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(welcome_label)
        
        # Description
        description = QLabel(
            "SatAnalytica is a comprehensive mission analysis platform designed specifically for "
            "engineers and mission planners working with CubeSat deployments.\n\n"
            "This professional-grade desktop application transforms complex satellite communication "
            "calculations into an intuitive workflow while providing unparalleled depth of analysis.\n\n"
            "Choose an analysis type below to begin your calculations."
        )
        description.setObjectName("welcomeDescription")
        description.setWordWrap(True)
        description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(description)
        
        # Add spacing after description
        main_layout.addSpacing(20)
        
        # Container for analysis options
        options_container = QWidget()
        grid_layout = QGridLayout(options_container)
        
        # Set equal spacing between all cells (both horizontal and vertical)
        grid_layout.setHorizontalSpacing(40)
        grid_layout.setVerticalSpacing(40)
        grid_layout.setContentsMargins(20, 20, 20, 20)
        
        # Analysis options
        analysis_options = [
            {
                "title": "Link Budget Analysis",
                "click_handler": self.parent.show_link_budget,
                "enabled": True
            },
            {
                "title": "Data Budget Analysis",
                "click_handler": self.parent.show_data_budget,
                "enabled": True
            },
            {
                "title": "Mass Budget Analysis",
                "click_handler": self.parent.show_mass_budget,
                "enabled": False,
                "tooltip": "Mass Budget Analysis will be available in a future update"
            },
            {
                "title": "Power Budget Analysis",
                "click_handler": self.parent.show_power_budget,
                "enabled": False,
                "tooltip": "Power Budget Analysis will be available in a future update"
            },
            {
                "title": "Thermal Analysis Budget",
                "click_handler": self.parent.show_thermal_budget,
                "enabled": False,
                "tooltip": "Thermal Analysis Budget will be available in a future update"
            }
        ]
        
        # Add analysis buttons to grid
        for i, option in enumerate(analysis_options):
            row = i // 2
            col = i % 2
            button = AnalysisButton(option["title"])
            
            if option["enabled"]:
                button.clicked.connect(option["click_handler"])
            else:
                # For disabled features, show tooltip and use custom handler
                button.setProperty("inactive", True)
                button.setToolTip(option["tooltip"])
                button.clicked.connect(lambda checked, msg=option["tooltip"]: 
                    QMessageBox.information(self, "Feature Coming Soon", msg))
                button.setStyleSheet("""
                    AnalysisButton[inactive="true"] {
                        background-color: #1d1d1d;
                        border: 2px solid #333;
                        border-radius: 10px;
                        padding: 15px;
                        color: #666;
                        font-size: 16px;
                        font-weight: bold;
                        font-family: 'Segoe UI', 'Roboto', sans-serif;
                    }
                    AnalysisButton[inactive="true"]:hover {
                        background-color: #1d1d1d;
                        border-color: #333;
                        color: #666;
                    }
                """)
            grid_layout.addWidget(button, row, col)
        
        main_layout.addWidget(options_container, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Add stretching space before back button
        main_layout.addStretch(1)
        
        # Back button container
        back_container = QFrame()
        back_container.setObjectName("backContainer")
        back_layout = QHBoxLayout(back_container)
        back_layout.setContentsMargins(0, 20, 0, 0)  # Add top margin to back button
        
        back_btn = QPushButton("← Back to Login")
        back_btn.setObjectName("backButton")
        back_btn.clicked.connect(self.parent.show_login_page)
        back_layout.addWidget(back_btn, alignment=Qt.AlignmentFlag.AlignLeft)
        
        main_layout.addWidget(back_container)
        
        # Set stylesheet
        self.setStyleSheet("""
            QWidget {
                background-color: #1E1E1E;
            }
            
            QLabel#welcomeTitle {
                color: #4CAF50;
                font-family: 'Segoe UI', 'Roboto', sans-serif;
                font-size: 32px;
                font-weight: bold;
                margin-bottom: 25px;
            }
            
            QLabel#welcomeDescription {
                color: #FFFFFF;
                font-family: 'Segoe UI', 'Roboto', sans-serif;
                font-size: 16px;
                line-height: 1.6;
                margin-bottom: 30px;
                padding: 0 40px;
            }
            
            QPushButton#backButton {
                background-color: transparent;
                color: #4CAF50;
                border: 2px solid #4CAF50;
                border-radius: 5px;
                padding: 10px 20px;
                font-family: 'Segoe UI', 'Roboto', sans-serif;
                font-size: 14px;
                font-weight: bold;
            }
            
            QPushButton#backButton:hover {
                background-color: #4CAF50;
                color: white;
            }
            
            AnalysisButton {
                background-color: #2d2d2d;
                border: 2px solid #444;
                border-radius: 10px;
                padding: 15px;
                color: white;
                font-size: 16px;
                font-weight: bold;
                font-family: 'Segoe UI', 'Roboto', sans-serif;
            }
            
            AnalysisButton:hover {
                background-color: #3d3d3d;
                border-color: #4CAF50;
            }
            
            AnalysisButton:pressed {
                background-color: #262626;
            }
        """) 