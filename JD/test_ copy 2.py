# -*- coding: utf-8 -*-
import sys
import sqlite3
from PyQt5.QtCore import Qt, pyqtSignal, QThread
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit,
                             QPushButton, QComboBox, QListWidget, QSplitter, QMessageBox, QFileDialog, QTextEdit,
                             QSizePolicy, QHBoxLayout, QGridLayout, QScrollArea)
from PyQt5.QtGui import QPixmap, QImage
import os
import ftplib

class FTP_Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ftp = None  # Initialize the ftp attribute to None first
        self.search_query = ""
        self.search_query_end = ""
        try:
            self.ftp = ftplib.FTP('127.0.0.1', user='admin', passwd='1234', timeout=30)
            print(f"FTP initialized: {self.ftp}")  # Debugging line
        except ftplib.all_errors as e:
            print(f"FTP connection error: {e}")
        self.initUI()
        self.load_image_paths()
        
    def initUI(self):
        self.setWindowTitle('FTP 브라우저')
        self.resize(1920, 1080)

        splitter = QSplitter(Qt.Horizontal)

        self.file_list_widget = QListWidget()
        self.file_list_widget.setDragEnabled(True)
        self.file_list_widget.itemDoubleClicked.connect(self.display_image)
        self.load_ftp_image_paths()
        if hasattr(self, 'image_paths'):
            self.file_list_widget.addItems(self.image_paths)

        self.image_label = QLabel()
        self.image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setScaledContents(True)
        self.image_label.setFixedWidth(1600)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.image_label)

        self.search_input = QLineEdit()
        self.search_input.textChanged.connect(self.search_images)

        self.search_input_label = QLabel()
        self.search_input_label.setText("앞에서 검색")
        # self.search_button = QPushButton("앞에서 검색")
        # self.search_button.clicked.connect(self.search_images)
        
        self.search_input_end_label = QLabel()
        self.search_input_end_label.setText("뒤자리에서 검색")
        self.search_input_end = QLineEdit()
        self.search_input_end.textChanged.connect(self.search_images_end)

        # self.search_button_end = QPushButton("뒷자리 검색")
        # self.search_button_end.clicked.connect(self.search_images_end)

        button_layout = QGridLayout()
        button_layout.addWidget(self.search_input_label, 0, 0)
        button_layout.addWidget(self.search_input, 0, 1)
        button_layout.addWidget(self.search_input_end_label, 1, 0)
        button_layout.addWidget(self.search_input_end, 1, 1)

        splitter.addWidget(self.file_list_widget)
        splitter.addWidget(self.scroll_area)

        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(splitter)
        layout.addLayout(button_layout)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def display_image(self, item):
        try:
            # Load the image from the file path provided in the item
            pixmap = QPixmap(item.text())
            if pixmap.isNull():
                raise ValueError(f"Could not load image from {item.text()}")
            
            # Set the pixmap to the image label and adjust its size
            self.image_label.setPixmap(pixmap)
            self.image_label.setScaledContents(True)
            self.image_label.adjustSize()
            
            # Limit the size of the image label
            max_width = 600
            max_height = 400
            if pixmap.width() > max_width or pixmap.height() > max_height:
                scaled_pixmap = pixmap.scaled(max_width, max_height, Qt.IgnoreAspectRatio)
                self.image_label.setPixmap(scaled_pixmap)
        except Exception as e:
            print(f"Error displaying image: {e}")

    def show_image(self, item):
        self.display_image(item)

    def load_image_paths(self):
        with sqlite3.connect('image_db.db') as conn:
            c = conn.cursor()
            if self.search_query:
                c.execute(f"SELECT path FROM images WHERE front LIKE '{self.search_query}%'")
            elif self.search_query_end:
                c.execute(f"SELECT path FROM images WHERE back LIKE '{self.search_query_end}%'")
            else:
                c.execute("SELECT path FROM images")
            image_paths = [row[0] for row in c.fetchall()]
        self.image_paths = image_paths
        
    def load_ftp_image_paths(self):
        if self.ftp is None:
            print("FTP connection is not initialized")
            return
        try:
            file_list = self.ftp.nlst()
            current_directory = 'C:/Users/Administrator/Desktop/ftp_folder/'
            self.image_paths = [os.path.join(current_directory, path) for path in file_list]
            self.conn = sqlite3.connect('image_db.db')
            self.cursor = self.conn.cursor()
            self.cursor.execute('CREATE TABLE IF NOT EXISTS images (name TEXT PRIMARY KEY , time TEXT, plate TEXT, path TEXT, front TEXT, back TEXT)')
            for i in self.image_paths:
                path = i
                name = i.split('/')[-1]
                time = name.split('_')[0]
                plate = name.split('_')[1].split('.')[0]
                front = None
                back = None
                if len(plate) == 7:
                    front = plate[:2]
                    back = plate[3:]
                elif len(plate) == 8:
                    front = plate[:3]
                    back = plate[4:]
                self.cursor.execute('INSERT OR IGNORE INTO images (name, time, plate, path, front, back) VALUES (?,?,?,?,?,?)', (name, time, plate, path, front, back))
            self.conn.commit()

        except ftplib.all_errors as e:
            print(f"Error loading FTP image paths: {e}")
        finally:
            self.ftp.quit()

    def search_images(self):
        self.search_query = self.search_input.text()
        self.load_image_paths()
        self.file_list_widget.clear()
        self.file_list_widget.addItems(self.image_paths)

    def search_images_end(self):
        self.search_query_end = self.search_input_end.text()
        self.load_image_paths()
        self.file_list_widget.clear()
        self.file_list_widget.addItems(self.image_paths)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FTP_Browser()
    window.show()
    sys.exit(app.exec_())
