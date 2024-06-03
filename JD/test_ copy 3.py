import sys
import sqlite3
from PyQt5.QtCore import Qt, pyqtSignal, QThread
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit,
                             QPushButton, QComboBox, QListWidget, QSplitter, QMessageBox, QFileDialog, QTextEdit,
                             QSizePolicy, QHBoxLayout, QGridLayout, QScrollArea, QFrame)
from PyQt5.QtGui import QPixmap, QImage
import os
import ftplib

class FTP_Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ftp = None  # Initialize the ftp attribute to None first
        self.selected_images = []  # List to store selected images
        self.num_images_to_show = 1  # Number of images to show initially
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

        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.setSizes([300, 500])
        self.button_show_one = QPushButton("1개 보기", clicked=self.show_one_image)
        self.button_show_two = QPushButton("2개 보기", clicked=self.show_two_images)
        self.button_show_four = QPushButton("4개 보기", clicked=self.show_four_images)
    

        self.file_list_widget = QListWidget()
        self.file_list_widget.setDragEnabled(True)
        self.file_list_widget.itemDoubleClicked.connect(self.display_image)
        self.load_ftp_image_paths()
        if hasattr(self, 'image_paths'):
            self.file_list_widget.addItems(self.image_paths)

        self.image_labels = []  # List to store the image labels
        self.scroll_areas = []  # List to store the scroll areas
        self.init_image_display()

        self.search_input_front = QLineEdit()
        self.search_input_front.setPlaceholderText("Search by front")
        self.search_input_front.textChanged.connect(self.search_images)

        self.search_input_back = QLineEdit()
        self.search_input_back.setPlaceholderText("Search by back")
        self.search_input_back.textChanged.connect(self.search_images)

        list_widget_layout = QVBoxLayout()
        list_widget_layout.addWidget(self.button_show_one)
        list_widget_layout.addWidget(self.button_show_two)
        list_widget_layout.addWidget(self.button_show_four)
        list_widget_layout.addWidget(self.file_list_widget)

        list_widget_container = QWidget()
        list_widget_container.setLayout(list_widget_layout)

        self.splitter.addWidget(list_widget_container)
        self.splitter.addWidget(self.image_display_widget)

        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.splitter)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
    def display_image(self, item):
        try:
            pixmap = QPixmap(item.text())
            if pixmap.isNull():
                raise ValueError(f"Could not load image from {item.text()}")
            
            for i in range(self.num_images_to_show):
                if i < len(self.image_labels):
                    image_path = self.image_paths[i] if i < len(self.image_paths) else ""
                    pixmap = QPixmap(image_path)
                    if pixmap.isNull():
                        self.image_labels[i].clear()
                    else:
                        self.image_labels[i].setPixmap(pixmap)
                        self.image_labels[i].setScaledContents(True)
                        self.image_labels[i].adjustSize()
                        # Limit the size of the image label
                        max_width = 600
                        max_height = 400
                        if pixmap.width() > max_width or pixmap.height() > max_height:
                            scaled_pixmap = pixmap.scaled(max_width, max_height, Qt.IgnoreAspectRatio)
                            self.image_labels[i].setPixmap(scaled_pixmap)
                else:
                    self.image_labels[i].clear()
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
        query_front = self.search_input_front.text().lower()
        query_back = self.search_input_back.text().lower()
        self.search_query = query_front
        self.search_query_end = query_back

        self.load_image_paths()
        filtered_paths = [path for path in self.image_paths if query_front in os.path.basename(path).lower() and query_back in os.path.basename(path).lower()]
        self.file_list_widget.clear()
        self.file_list_widget.addItems(filtered_paths)

    def init_image_display(self):
        # Create initial image labels and scroll areas
        self.image_display_widget = QWidget()
        self.image_layout = QVBoxLayout()
        for i in range(4):  # Initialize with max number of image views possible
            label = QLabel()
            label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            label.setAlignment(Qt.AlignCenter)
            label.setScaledContents(True)
            label.setFixedWidth(1600)
            self.image_labels.append(label)

            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)
            scroll_area.setWidget(label)
            self.scroll_areas.append(scroll_area)
            self.image_layout.addWidget(scroll_area)

        self.image_display_widget.setLayout(self.image_layout)
        self.update_image_display()

    def update_image_display(self):
        for i in range(len(self.image_labels)):
            if i < self.num_images_to_show:
                self.scroll_areas[i].show()
            else:
                self.scroll_areas[i].hide()

    def show_one_image(self):
        self.num_images_to_show = 1
        self.update_image_display()

    def show_two_images(self):
        self.num_images_to_show = 2
        self.update_image_display()

    def show_four_images(self):
        self.num_images_to_show = 4
        self.image_layout.setAlignment(Qt.AlignTop)
        self.image_layout.setSpacing(0)
        self.image_layout.setContentsMargins(0, 0, 0, 0)
        for i in range(4):
            self.image_layout.takeAt(2)
        for i in range(0, 4, 2):
            hbox = QHBoxLayout()
            hbox.setAlignment(Qt.AlignTop)
            hbox.setSpacing(0)
            hbox.setContentsMargins(0, 0, 0, 0)
            hbox.addWidget(self.scroll_areas[i])
            if i+1 < self.num_images_to_show:
                hbox.addWidget(self.scroll_areas[i+1])
            self.image_layout.addLayout(hbox)
        for i in range(self.image_layout.count()):
            self.image_layout.setStretchFactor(self.image_layout.itemAt(i).widget(), 1)
        self.update_image_display()
        self.update_image_display()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FTP_Browser()
    window.show()
    sys.exit(app.exec_())


