import yt_dlp
from PySide6.QtCore import QObject, Signal, QThread

class DownloaderWorker(QObject):
    progress = Signal(dict)
    finished = Signal()
    download_error = Signal(str)
    log = Signal(str)

    def __init__(self, url, options):
        super().__init__()
        self.url = url
        self.options = options
        self._is_cancelled = False

    def run(self):
        # Inject progress hook
        self.options['progress_hooks'] = [self._progress_hook]
        self.options['logger'] = self
        
        try:
            with yt_dlp.YoutubeDL(self.options) as ydl:
                ydl.download([self.url])
            if not self._is_cancelled:
                self.finished.emit()
        except Exception as e:
            self.download_error.emit(str(e))

    def _progress_hook(self, d):
        if self._is_cancelled:
            raise yt_dlp.utils.DownloadError("Download cancelled")
        if d['status'] == 'downloading':
            self.progress.emit(d)
        elif d['status'] == 'finished':
            self.log.emit("Download finished, processing...")

    def debug(self, msg):
        if not msg.startswith('[debug] '):
            self.log.emit(msg)

    def info(self, msg):
        self.log.emit(msg)

    def warning(self, msg):
        self.log.emit(f"Warning: {msg}")

    def error(self, msg):
        self.log.emit(f"Error: {msg}")

    def cancel(self):
        self._is_cancelled = True

class YtDownloader:
    @staticmethod
    def get_info(url):
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            return ydl.extract_info(url, download=False)

    @staticmethod
    def extract_playlist_flat(url):
        opts = {
            'extract_flat': True,  # Don't resolve every video, just get the list
            'quiet': True,
        }
        with yt_dlp.YoutubeDL(opts) as ydl:
            return ydl.extract_info(url, download=False)
