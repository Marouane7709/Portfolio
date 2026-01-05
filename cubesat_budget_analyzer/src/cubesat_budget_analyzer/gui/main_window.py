"""Main window for the SatAnalytica application."""

from PyQt6.QtWidgets import (QMainWindow, QWidget, QStackedWidget, QVBoxLayout,
                           QMenuBar, QStatusBar, QMessageBox, QFileDialog, QTabWidget,
                           QLabel, QHBoxLayout, QApplication)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
from .login_page import LoginPage
from .home_page import HomePage
from .tabs import LinkBudgetTab, DataBudgetTab
from utils.file_manager import FileManager
from utils.report_generator import ReportGenerator

class MainWindow(QMainWindow):
    """Main window class for the application."""
    
    def __init__(self):
        super().__init__()
        self.file_manager = FileManager()
        self.report_generator = ReportGenerator()
        self.autosave_timer = QTimer()
        self.setWindowTitle("CubeSat Budget Analyzer")
        self.setMinimumSize(1200, 800)
        self.init_ui()
        self.setup_autosave()
    
    def init_ui(self):
        """Initialize the user interface."""
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Center the window on screen
        screen = QApplication.primaryScreen().geometry()
        window_geometry = self.geometry()
        x = (screen.width() - window_geometry.width()) // 2
        y = (screen.height() - window_geometry.height()) // 2
        self.move(x, y)
        
        # Create stacked widget for pages
        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget)
        
        # Create pages
        self.login_page = LoginPage(self)
        self.home_page = HomePage(self)
        
        # Create tab widget for analysis tabs
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #444;
                background: #2d2d2d;
            }
            QTabBar::tab {
                background: #333;
                color: #fff;
                border: 1px solid #444;
                padding: 8px 16px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background: #2d2d2d;
                border-bottom: none;
            }
            QTabBar::tab:hover {
                background: #3d3d3d;
            }
        """)
        
        # Create tabs
        self.link_budget_tab = LinkBudgetTab(self)
        self.data_budget_tab = DataBudgetTab(self)
        
        # Add tabs to tab widget
        self.tab_widget.addTab(self.link_budget_tab, "Link Budget Analysis")
        # Initially only show Link Budget tab
        
        # Add pages to stacked widget
        self.stacked_widget.addWidget(self.login_page)
        self.stacked_widget.addWidget(self.home_page)
        self.stacked_widget.addWidget(self.tab_widget)
        
        # Show login page initially
        self.stacked_widget.setCurrentWidget(self.login_page)
        
        # Set window style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
                color: #ffffff;
            }
            QGroupBox {
                border: 1px solid #444;
                border-radius: 4px;
                margin-top: 1ex;
                font-weight: bold;
                color: #ffffff;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px 0 3px;
                color: #ffffff;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
            QLabel {
                color: #ffffff;
            }
            QLineEdit, QSpinBox, QDoubleSpinBox {
                padding: 5px;
                border: 1px solid #444;
                border-radius: 4px;
                background-color: #333;
                color: #ffffff;
            }
            QComboBox {
                border: 1px solid #444;
                border-radius: 4px;
                padding: 5px;
                background-color: #333;
                color: #ffffff;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: url(down_arrow.png);
                width: 12px;
                height: 12px;
            }
            QCheckBox {
                color: #ffffff;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
            }
            QCheckBox::indicator:unchecked {
                border: 1px solid #444;
                background-color: #333;
            }
            QCheckBox::indicator:checked {
                border: 1px solid #444;
                background-color: #4CAF50;
            }
        """)
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create status bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Ready")
    
    def create_menu_bar(self):
        """Create the application menu bar."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        
        new_action = file_menu.addAction("New Project")
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.new_project)
        
        open_action = file_menu.addAction("Open Project")
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_project)
        
        save_action = file_menu.addAction("Save Project")
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_project)
        
        file_menu.addSeparator()
        
        export_menu = file_menu.addMenu("Export Report")
        export_pdf = export_menu.addAction("Export as PDF")
        export_pdf.triggered.connect(lambda: self.export_report("pdf"))
        export_json = export_menu.addAction("Export as JSON")
        export_json.triggered.connect(lambda: self.export_report("json"))
        
        file_menu.addSeparator()
        
        exit_action = file_menu.addAction("Exit")
        exit_action.setShortcut("Alt+F4")
        exit_action.triggered.connect(self.close)
        
        # Edit menu
        edit_menu = menubar.addMenu("Edit")
        preferences = edit_menu.addAction("Preferences")
        preferences.triggered.connect(self.show_preferences)
        
        # View menu
        view_menu = menubar.addMenu("View")
        toggle_dark = view_menu.addAction("Toggle Dark Mode")
        toggle_dark.setShortcut("Ctrl+D")
        toggle_dark.triggered.connect(self.toggle_dark_mode)
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        docs = help_menu.addAction("Documentation")
        docs.triggered.connect(self.show_documentation)
        about = help_menu.addAction("About")
        about.triggered.connect(self.show_about)
    
    def setup_autosave(self):
        """Set up autosave functionality."""
        self.autosave_timer.timeout.connect(self.autosave)
        self.autosave_timer.start(5 * 60 * 1000)  # Autosave every 5 minutes
    
    def autosave(self):
        """Perform autosave."""
        try:
            data = {
                "link_budget": self.link_budget_tab.get_data(),
                "data_budget": self.data_budget_tab.get_data()
            }
            self.file_manager.save_project("autosave", data)
            self.statusBar.showMessage("Project autosaved", 3000)
        except Exception as e:
            self.statusBar.showMessage(f"Autosave failed: {str(e)}", 3000)
    
    def new_project(self):
        """Create a new project."""
        self.link_budget_tab.clear_inputs()
        self.data_budget_tab.clear_inputs()
        self.statusBar.showMessage("New project created")
    
    def save_project(self):
        """Save the current project."""
        try:
            data = {
                "link_budget": self.link_budget_tab.get_data(),
                "data_budget": self.data_budget_tab.get_data()
            }
            
            filename, _ = QFileDialog.getSaveFileName(
                self,
                "Save Project",
                "",
                "JSON Files (*.json)"
            )
            
            if filename:
                name = filename.split("/")[-1].replace(".json", "")
                filepath = self.file_manager.save_project(name, data)
                self.statusBar.showMessage(f"Project saved to {filepath}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save project: {str(e)}")
    
    def open_project(self):
        """Open an existing project."""
        try:
            filename, _ = QFileDialog.getOpenFileName(
                self,
                "Open Project",
                str(self.file_manager.projects_dir),
                "JSON Files (*.json)"
            )
            
            if filename:
                data = self.file_manager.load_project(filename)
                self.link_budget_tab.set_data(data.get("link_budget", {}))
                self.data_budget_tab.set_data(data.get("data_budget", {}))
                self.statusBar.showMessage(f"Project loaded from {filename}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load project: {str(e)}")
    
    def export_report(self, format: str):
        """Export analysis results to a report."""
        try:
            data = {
                "link_budget": self.link_budget_tab.get_data(),
                "data_budget": self.data_budget_tab.get_data()
            }
            
            if format == "pdf":
                filename, _ = QFileDialog.getSaveFileName(
                    self,
                    "Export PDF Report",
                    "",
                    "PDF Files (*.pdf)"
                )
                if filename:
                    self.report_generator.generate_pdf(data, filename)
                    self.statusBar.showMessage(f"Report exported to {filename}")
            elif format == "json":
                filepath = self.file_manager.export_report(data, format="json")
                self.statusBar.showMessage(f"Report exported to {filepath}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to export report: {str(e)}")
    
    def show_preferences(self):
        """Show the preferences dialog."""
        QMessageBox.information(
            self,
            "Preferences",
            "Preferences dialog will be available in a future update."
        )
    
    def toggle_dark_mode(self):
        """Toggle dark mode."""
        QMessageBox.information(
            self,
            "Dark Mode",
            "Dark mode will be available in a future update."
        )
    
    def show_documentation(self):
        """Show the documentation."""
        QMessageBox.information(
            self,
            "Documentation",
            "Please visit our documentation website for detailed information about using the application."
        )
    
    def show_about(self):
        """Show the about dialog."""
        QMessageBox.about(
            self,
            "About SatAnalytica",
            """
            <h3>SatAnalytica v1.0.0</h3>
            <p>A comprehensive tool for analyzing CubeSat link and data budgets.</p>
            <p>© 2024 Your Organization</p>
            """
        )
    
    def show_login_page(self):
        """Show the login page."""
        self.stacked_widget.setCurrentWidget(self.login_page)
    
    def show_home_page(self):
        """Show the home page."""
        self.stacked_widget.setCurrentWidget(self.home_page)
    
    def show_link_budget(self):
        """Show the link budget analysis tab."""
        self.stacked_widget.setCurrentWidget(self.tab_widget)
        # Clear existing tabs
        while self.tab_widget.count() > 0:
            self.tab_widget.removeTab(0)
        # Add only the Link Budget tab
        self.tab_widget.addTab(self.link_budget_tab, "Link Budget Analysis")
        self.tab_widget.tabBar().setVisible(False)
    
    def show_data_budget(self):
        """Show the data budget analysis tab."""
        self.stacked_widget.setCurrentWidget(self.tab_widget)
        # Clear existing tabs
        while self.tab_widget.count() > 0:
            self.tab_widget.removeTab(0)
        # Add only the Data Budget tab
        self.tab_widget.addTab(self.data_budget_tab, "Data Budget Analysis")
        self.tab_widget.tabBar().setVisible(False)
        
    def show_mass_budget(self):
        """Show the mass budget analysis tab."""
        QMessageBox.information(
            self,
            "Feature Coming Soon",
            "Mass Budget Analysis will be available in a future update."
        )
        
    def show_power_budget(self):
        """Show the power budget analysis tab."""
        QMessageBox.information(
            self,
            "Feature Coming Soon",
            "Power Budget Analysis will be available in a future update."
        )
        
    def show_thermal_budget(self):
        """Show the thermal analysis budget tab."""
        QMessageBox.information(
            self,
            "Feature Coming Soon",
            "Thermal Analysis Budget will be available in a future update."
        ) 