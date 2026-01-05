"""Main entry point for SatAnalytica."""

import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from cubesat_budget_analyzer.gui.main_window import MainWindow

def main():
    """Main entry point for the application."""
    # Enable High DPI support
    if hasattr(Qt, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    # Create application
    app = QApplication(sys.argv)
    
    # Create main window
    main_window = MainWindow()
    
    # Show window
    main_window.show()
    
    # Start event loop
    return app.exec()

if __name__ == '__main__':
    sys.exit(main()) 