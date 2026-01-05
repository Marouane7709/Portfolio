"""Login page for the CubeSat Budget Analyzer."""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
                           QLabel, QPushButton, QLineEdit, QMessageBox,
                           QCheckBox, QFrame, QProgressBar)
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, pyqtProperty
from PyQt6.QtGui import QFont, QIcon, QPixmap
import os

class LoginPage(QWidget):
    """Login page widget."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()
        self.setup_animations()
    
    def init_ui(self):
        """Initialize the user interface."""
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.setSpacing(0)
        self.setLayout(main_layout)
        
        # Logo container
        logo_container = QFrame()
        logo_container.setObjectName("logoContainer")
        logo_layout = QVBoxLayout(logo_container)
        logo_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Logo image with fallback
        logo_label = QLabel()
        logo_label.setObjectName("logoLabel")
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Try to load the logo, if it exists
        logo_path = os.path.join(os.path.dirname(__file__), "..", "..", "assets", "logo.png")
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            if not pixmap.isNull():
                logo_label.setPixmap(pixmap.scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio))
        else:
            # Create a placeholder logo using text
            logo_label.setText("🚀")
            logo_label.setStyleSheet("""
                QLabel#logoLabel {
                    font-size: 80px;
                    color: #4CAF50;
                    margin-bottom: 20px;
                }
            """)
        
        logo_layout.addWidget(logo_label)
        
        # Title
        title_label = QLabel("CubeSat Budget Analyzer")
        title_label.setFont(QFont('Segoe UI', 24, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #4CAF50; margin-bottom: 10px;")
        logo_layout.addWidget(title_label)
        
        # Subtitle
        subtitle_label = QLabel("Satellite Communication and Data Budget Analysis Tool")
        subtitle_label.setFont(QFont('Segoe UI', 12))
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setStyleSheet("color: #cccccc; margin-bottom: 20px;")
        logo_layout.addWidget(subtitle_label)
        
        main_layout.addWidget(logo_container)
        
        # Login form container
        self.form_container = QFrame()
        self.form_container.setObjectName("formContainer")
        self.form_container.setMaximumWidth(400)
        form_layout = QVBoxLayout(self.form_container)
        form_layout.setSpacing(15)
        form_layout.setContentsMargins(30, 30, 30, 30)
        
        # Username field
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter username")
        self.username_input.setObjectName("inputField")
        self.username_input.textChanged.connect(self.validate_inputs)
        form_layout.addWidget(self.username_input)
        
        # Password field
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setObjectName("inputField")
        self.password_input.textChanged.connect(self.validate_inputs)
        form_layout.addWidget(self.password_input)
        
        # Remember me and forgot password
        options_layout = QHBoxLayout()
        
        self.remember_me = QCheckBox("Remember me")
        self.remember_me.setObjectName("rememberMe")
        options_layout.addWidget(self.remember_me)
        
        self.forgot_password = QPushButton("Forgot Password?")
        self.forgot_password.setObjectName("forgotPassword")
        self.forgot_password.clicked.connect(self.handle_forgot_password)
        options_layout.addWidget(self.forgot_password)
        
        form_layout.addLayout(options_layout)
        
        # Login button
        self.login_button = QPushButton("Login")
        self.login_button.setObjectName("loginButton")
        self.login_button.clicked.connect(self.login)
        self.login_button.setEnabled(False)
        form_layout.addWidget(self.login_button)
        
        # Progress bar (initially hidden)
        self.progress_bar = QProgressBar()
        self.progress_bar.setObjectName("progressBar")
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.hide()
        form_layout.addWidget(self.progress_bar)
        
        main_layout.addWidget(self.form_container, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Set stylesheet
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
            }
            
            QFrame#logoContainer {
                background-color: transparent;
                margin-bottom: 40px;
            }
            
            QFrame#formContainer {
                background-color: #2d2d2d;
                border-radius: 10px;
                border: 1px solid #444;
            }
            
            QLineEdit#inputField {
                padding: 12px;
                border: 1px solid #444;
                border-radius: 6px;
                background-color: #333;
                color: #ffffff;
                font-size: 14px;
            }
            
            QLineEdit#inputField:focus {
                border: 1px solid #4CAF50;
            }
            
            QCheckBox#rememberMe {
                color: #cccccc;
                font-size: 13px;
            }
            
            QPushButton#forgotPassword {
                color: #4CAF50;
                border: none;
                background: transparent;
                font-size: 13px;
                text-decoration: underline;
            }
            
            QPushButton#forgotPassword:hover {
                color: #45a049;
            }
            
            QPushButton#loginButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 12px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 14px;
            }
            
            QPushButton#loginButton:hover {
                background-color: #45a049;
            }
            
            QPushButton#loginButton:disabled {
                background-color: #333;
                color: #666;
            }
            
            QProgressBar#progressBar {
                border: none;
                background-color: #333;
                border-radius: 3px;
                height: 3px;
            }
            
            QProgressBar#progressBar::chunk {
                background-color: #4CAF50;
                border-radius: 3px;
            }
        """)
    
    def setup_animations(self):
        """Setup animations for the login form."""
        self.form_animation = QPropertyAnimation(self.form_container, b"geometry")
        self.form_animation.setDuration(500)
        self.form_animation.setEasingCurve(QEasingCurve.Type.OutBack)
        
        self.progress_animation = QPropertyAnimation(self.progress_bar, b"value")
        self.progress_animation.setDuration(1000)
        self.progress_animation.setStartValue(0)
        self.progress_animation.setEndValue(100)
    
    def validate_inputs(self):
        """Validate the input fields and enable/disable login button."""
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        self.login_button.setEnabled(bool(username and password))
    
    def login(self):
        """Handle login button click."""
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        
        if not username or not password:
            QMessageBox.warning(
                self,
                "Login Failed",
                "Please enter both username and password."
            )
            return
        
        # Show progress bar and start animation
        self.progress_bar.show()
        self.progress_animation.start()
        
        # Simulate login process
        QTimer.singleShot(1500, self.complete_login)
    
    def complete_login(self):
        """Complete the login process."""
        self.progress_bar.hide()
        self.parent.show_home_page()
    
    def handle_forgot_password(self):
        """Handle forgot password button click."""
        QMessageBox.information(
            self,
            "Password Recovery",
            "Please contact your system administrator to reset your password."
        ) 