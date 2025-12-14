import sys
from PySide6.QtWidgets import QApplication
from gui.main_window import MainWindow
from gui.themes import DARK_STYLESHEET
import darkdetect

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    # Simple theme setup
    is_dark = True # Force dark for now or use darkdetect.isDark()
    if is_dark:
        app.setStyleSheet(DARK_STYLESHEET)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
