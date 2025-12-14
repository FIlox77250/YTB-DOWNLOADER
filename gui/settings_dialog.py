from PySide6.QtWidgets import (QDialog, QVBoxLayout, QLabel, QLineEdit, 
                               QPushButton, QHBoxLayout, QFormLayout)

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.resize(400, 200)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        
        form = QFormLayout()
        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText("Default Download Folder (Current Directory)")
        form.addRow("Download Path:", self.path_input)
        
        self.ffmpeg_input = QLineEdit()
        self.ffmpeg_input.setPlaceholderText("Path to ffmpeg executable (optional)")
        form.addRow("FFmpeg Path:", self.ffmpeg_input)
        
        layout.addLayout(form)
        
        btns = QHBoxLayout()
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        
        btns.addStretch()
        btns.addWidget(cancel_btn)
        btns.addWidget(save_btn)
        
        layout.addStretch()
        layout.addLayout(btns)
