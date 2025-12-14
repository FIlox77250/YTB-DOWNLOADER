from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                               QLineEdit, QPushButton, QListWidget, QListWidgetItem,
                               QComboBox, QLabel, QMessageBox, QFrame)
from PySide6.QtCore import Qt, QThread
from gui.widgets.video_card import VideoCard
from core.downloader import DownloaderWorker, YtDownloader
from gui.settings_dialog import SettingsDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YTB Downloader Pro")
        self.resize(1000, 700)
        
        self.init_ui()
        self.threads = [] # Keep references to threads

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # --- Header / Input Area ---
        input_frame = QFrame()
        input_frame.setObjectName("inputFrame")
        input_layout = QHBoxLayout(input_frame)
        
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Paste YouTube URL here...")
        self.url_input.setMinimumHeight(40)
        
        self.download_btn = QPushButton("Download")
        self.download_btn.setMinimumHeight(40)
        self.download_btn.setMinimumWidth(120)
        self.download_btn.clicked.connect(self.start_download)
        
        # Settings Button
        self.settings_btn = QPushButton("⚙")
        self.settings_btn.setObjectName("settingsBtn")
        self.settings_btn.setFixedSize(40, 40)
        self.settings_btn.setCursor(Qt.PointingHandCursor)
        self.settings_btn.clicked.connect(self.open_settings)
        
        input_layout.addWidget(self.url_input)
        input_layout.addWidget(self.download_btn)
        input_layout.addWidget(self.settings_btn)
        
        # --- Options Area ---
        options_layout = QHBoxLayout()
        # Clean spacing
        options_layout.setSpacing(15)
        
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Video + Audio", "Audio Only"])
        self.type_combo.setCursor(Qt.PointingHandCursor)
        
        self.quality_combo = QComboBox()
        self.quality_combo.addItems(["Best Available", "4K", "1080p", "720p"])
        self.quality_combo.setCursor(Qt.PointingHandCursor)
        
        options_layout.addWidget(QLabel("Type:"))
        options_layout.addWidget(self.type_combo)
        options_layout.addWidget(QLabel("Quality:"))
        options_layout.addWidget(self.quality_combo)
        options_layout.addStretch()
        
        # --- Queue Area ---
        queue_frame = QFrame()
        queue_frame.setObjectName("queueFrame")
        queue_layout = QVBoxLayout(queue_frame)
        queue_layout.setContentsMargins(1, 1, 1, 1) # Thin padding inside border
        
        queue_header = QLabel("Download Queue")
        queue_header.setObjectName("headerLabel")
        queue_header.setContentsMargins(10, 10, 0, 5)
        
        self.queue_list = QListWidget()
        self.queue_list.setSpacing(8) # Spacing between cards
        self.queue_list.setContentsMargins(5, 5, 5, 5)
        
        queue_layout.addWidget(queue_header)
        queue_layout.addWidget(self.queue_list)
        
        # Add widgets to main layout
        main_layout.addWidget(input_frame)
        main_layout.addLayout(options_layout)
        main_layout.addWidget(queue_frame)

    def open_settings(self):
        dlg = SettingsDialog(self)
        dlg.exec()

    def start_download(self):
        url = self.url_input.text().strip()
        if not url:
            return
            
        # Get Options
        format_type = self.type_combo.currentText()
        quality = self.quality_combo.currentText()
        
        self.download_btn.setEnabled(False) # Prevent spamming while fetching info
        
        # Simple check for playlist (could be better with regex or actual fetch)
        if "playlist" in url or "&list=" in url:
            # Run in thread to avoid UI freeze
            thread = QThread()
            # We can't put the static method directly in QThread easily without a worker
            # So we'll trigger a small helper worker. 
            # For simplicity in this demo, I will use a quick inline logical distinction
            # BUT: accessing network in main thread is bad. 
            # I'll modify things to fetch info in a thread.
             
            # Allow user to force single video or playlist
            msg = QMessageBox()
            msg.setWindowTitle("Playlist Detected")
            msg.setText("Do you want to download the whole playlist?")
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            ret = msg.exec()
            
            if ret == QMessageBox.Cancel:
                self.download_btn.setEnabled(True)
                return
            elif ret == QMessageBox.Yes:
                # Playlist mode
                self.process_playlist(url, format_type, quality)
                self.download_btn.setEnabled(True)
                return
        
        # Single Video (or user said No to playlist)
        self.add_download_task(url, format_type, quality)
        self.url_input.clear()
        self.download_btn.setEnabled(True)

    def process_playlist(self, url, format_type, quality):
        # NOTE: In a real app, this MUST be async. 
        # Flat extraction is fast but can still hang for 1-2s.
        try:
            info = YtDownloader.extract_playlist_flat(url)
            if 'entries' in info:
                for entry in info['entries']:
                    video_url = entry.get('url') or entry.get('webpage_url')
                    # 'url' in flat extraction is usually the ID, we need full link
                    if video_url:
                        # Construct full URL if it's just ID (common in flat)
                        if "youtube.com" not in video_url and "youtu.be" not in video_url:
                             video_url = f"https://www.youtube.com/watch?v={video_url}"
                        
                        self.add_download_task(video_url, format_type, quality)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to parse playlist: {str(e)}")

    def add_download_task(self, url, format_type, quality):
        # Create UI Card
        card = VideoCard(url) 
        
        item = QListWidgetItem(self.queue_list)
        item.setSizeHint(card.sizeHint())
        self.queue_list.setItemWidget(item, card)
        
        # Build options
        ydl_opts = {
            'outtmpl': '%(title)s.%(ext)s',
            'noplaylist': True,
            'writethumbnail': True,
            'addmetadata': True,
        }
        
        if format_type == "Audio Only":
            ydl_opts.update({
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            })
        else:
            # Video + Audio
            if quality == "4K":
                ydl_opts['format'] = 'bestvideo[height<=2160]+bestaudio/best[height<=2160]'
            elif quality == "1080p":
                ydl_opts['format'] = 'bestvideo[height<=1080]+bestaudio/best[height<=1080]'
            elif quality == "720p":
                ydl_opts['format'] = 'bestvideo[height<=720]+bestaudio/best[height<=720]'
            else:
                ydl_opts['format'] = 'bestvideo+bestaudio/best'
        
        # Create Worker Thread
        thread = QThread()
        worker = DownloaderWorker(url, ydl_opts)
        worker.moveToThread(thread)
        
        # Connect signals
        thread.started.connect(worker.run)
        worker.finished.connect(thread.quit)
        worker.finished.connect(worker.deleteLater)
        thread.finished.connect(thread.deleteLater)
        
        worker.progress.connect(card.update_progress)
        worker.download_error.connect(lambda e: card.status_label.setText(f"Error: {e}"))
        worker.log.connect(lambda msg: print(f"Log: {msg}")) # Simple logging for now
        
        # Keep track to prevent GC
        self.threads.append((thread, worker))
        
        thread.start()
