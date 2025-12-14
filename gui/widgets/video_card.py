from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QProgressBar, QPushButton
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, Signal
from core.utils import format_bytes

class VideoCard(QFrame):
    cancel_requested = Signal()

    def __init__(self, title, thumbnail_path=None):
        super().__init__()
        self.setObjectName("videoCard")
        self.setFixedHeight(100)
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)
        
        # Thumbnail (placeholder)
        self.thumb_label = QLabel()
        self.thumb_label.setFixedSize(120, 80)
        self.thumb_label.setStyleSheet("background-color: #333; border-radius: 5px;")
        if thumbnail_path:
             pixmap = QPixmap(thumbnail_path)
             if not pixmap.isNull():
                 self.thumb_label.setPixmap(pixmap.scaled(
                     self.thumb_label.size(), 
                     Qt.KeepAspectRatioByExpanding, 
                     Qt.SmoothTransformation
                 ))
        
        # Info Area
        info_layout = QVBoxLayout()
        self.title_label = QLabel(title)
        self.title_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        self.status_label = QLabel("Waiting...")
        self.status_label.setStyleSheet("color: #aaa;")
        
        info_layout.addWidget(self.title_label)
        info_layout.addWidget(self.status_label)
        info_layout.addStretch()
        
        # Progress Area
        prog_layout = QVBoxLayout()
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setTextVisible(False)
        self.speed_label = QLabel("")
        self.speed_label.setAlignment(Qt.AlignRight)
        
        prog_layout.addWidget(self.speed_label)
        prog_layout.addWidget(self.progress_bar)
        
        # Cancel Button
        self.cancel_btn = QPushButton("✕")
        self.cancel_btn.setObjectName("cancelBtn")
        self.cancel_btn.setFixedSize(30, 30)
        self.cancel_btn.clicked.connect(self.cancel_requested.emit)
        
        self.layout.addWidget(self.thumb_label)
        self.layout.addLayout(info_layout, stretch=1)
        self.layout.addLayout(prog_layout, stretch=0)
        self.layout.addWidget(self.cancel_btn)

    def update_progress(self, data):
        # data comes from yt-dlp progress hook
        if data['status'] == 'downloading':
            total = data.get('total_bytes') or data.get('total_bytes_estimate') or 0
            downloaded = data.get('downloaded_bytes', 0)
            if total > 0:
                percent = (downloaded / total) * 100
                self.progress_bar.setValue(int(percent))
                self.status_label.setText(f"{percent:.1f}%")
            
            speed = data.get('speed')
            if speed:
                self.speed_label.setText(f"{format_bytes(speed)}/s")
        
        elif data['status'] == 'finished':
            self.progress_bar.setValue(100)
            self.status_label.setText("Processing...")
            self.speed_label.setText("Done")
