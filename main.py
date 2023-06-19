from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QLineEdit, QFileDialog, QInputDialog
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt
import webbrowser
import pytube
import os
import shutil
from pathlib import Path

class BatchCreator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Batch File')
        self.setWindowIcon(QIcon('icon.png'))
        self.setGeometry(300, 300, 500, 300)  # Set the window size and position

        self.label = QLabel('Hello, User!', self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QFont('Arial', 18))

        self.button_link = QPushButton('Go to Website', self)
        self.button_download = QPushButton('Download File', self)
        self.button_convert = QPushButton('Convert Video to MP3', self)

        self.button_link.clicked.connect(self.openLink)
        self.button_download.clicked.connect(self.downloadFile)
        self.button_convert.clicked.connect(self.promptVideoLink)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button_link)
        layout.addWidget(self.button_download)
        layout.addWidget(self.button_convert)
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignCenter)

        self.setStyleSheet("""
    QWidget {
        background-color: #f5f5f5;
    }
    QPushButton {
        background-color: #4CAF50;
        color: white;
        padding: 10px 20px;
        font-size: 16px;
        border: none;
        border-radius: 4px;
        cursor: hand;  /* Change 'pointer' to 'hand' */
    }
    QPushButton:hover {
        background-color: #45a049;
    }
    QLineEdit {
        font-size: 16px;
        padding: 8px;
        border-radius: 4px;
        border: 1px solid #ccc;
    }
    """)

        self.setLayout(layout)

    def openLink(self):
        link, ok = QInputDialog.getText(self, 'Open Link', 'Enter the link:')
        if ok:
            webbrowser.open(link)

    def downloadFile(self):
        url, _ = QInputDialog.getText(self, 'Download File', 'Enter the file URL:')
        save_path, _ = QFileDialog.getSaveFileName(self, 'Save File', '', 'All Files (*)')
        if url and save_path:
            youtube = pytube.YouTube(url)
            stream = youtube.streams.first()
            stream.download(output_path=os.path.dirname(save_path), filename=os.path.basename(save_path))

    def promptVideoLink(self):
        link, ok = QInputDialog.getText(self, 'Convert Video to MP3', 'Paste the video link:')
        if ok:
            self.convertVideo(link)

    def convertVideo(self, url):
        save_path, _ = QFileDialog.getSaveFileName(self, 'Save MP3', '', 'Audio Files (*.mp3)')
        if save_path:
            youtube = pytube.YouTube(url)
            stream = youtube.streams.filter(only_audio=True).first()
            stream.download(output_path=os.path.dirname(save_path), filename=os.path.basename(save_path))

            # Move the converted file to the Downloads folder
            downloads_folder = str(Path.home() / "Downloads")
            new_file_path = os.path.join(downloads_folder, os.path.basename(save_path))
            shutil.move(save_path, new_file_path)

if __name__ == '__main__':
    app = QApplication([])
    window = BatchCreator()
    window.show()
    app.exec_()
