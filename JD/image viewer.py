import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileDialog, QApplication, QLabel, QWidget, QPushButton, QLineEdit, QListWidget, QAbstractItemView
from PyQt5.QtGui import QPixmap
import sqlite3
from collections import deque
import os 
import ftplib


class ImageViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Viewer")
        self.resize(1920, 1080)
        
        try:
            self.ftp = ftplib.FTP('127.0.0.1', user='admin', passwd='1234', timeout=30)
            print(f"FTP initialized: {self.ftp}")  # Debugging line
        except ftplib.all_errors as e:
            print(f"FTP connection error: {e}")
            
        self.split_mode = 1
        self.selected_images = deque(maxlen=4)
        self.search_query = ""
        self.search_query_end = ""
        self.load_ftp_image_paths()
        self.load_image_paths()
        
        
        self.one_button = QPushButton("1", self)
        self.one_button.resize(30, 30)  # Set size
        self.one_button.move(10, 40)  # Set position

        self.two_button = QPushButton("2", self)
        self.two_button.resize(30, 30)
        self.two_button.move(50, 40)  # Set position

        self.four_button = QPushButton("4", self)
        self.four_button.resize(30, 30)
        self.four_button.move(90, 40)  # Set position
        
        self.clear_selection_button = QPushButton('Clear', self)
        self.clear_selection_button.resize(70, 30)
        self.clear_selection_button.move(130, 40)
        
        self.one_button.clicked.connect(lambda: self.set_selection(1))
        self.one_button.clicked.connect(self.display_images)
        self.two_button.clicked.connect(lambda: self.set_selection(2))
        self.two_button.clicked.connect(self.display_images)
        self.four_button.clicked.connect(lambda: self.set_selection(4))
        self.four_button.clicked.connect(self.display_images)
        
        self.image_list = QListWidget(self)
        self.image_list.move(10, 130)  # Set position
        self.image_list.resize(200, 400)
        self.image_list.itemDoubleClicked.connect(self.add_image)  # Connect the clicked signal
        self.image_list.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.image_list.setDragEnabled(True)
        self.clear_selection_button.clicked.connect(self.image_list.clearSelection)
        
        if hasattr(self, 'image_paths'):
            self.image_list.addItems(self.image_paths)
        
        self.one_label = QLabel(self)
        self.one_label.setScaledContents(True)  # Enable image scaling
        self.one_label.setFixedSize(1000, 800)  # Set fixed size
        self.one_label.move(250, 130)

        self.two_labels = [QLabel(self), QLabel(self)]
        for label in self.two_labels:
            label.setScaledContents(True)
            label.setFixedSize(600, 400)
        self.two_labels[0].move(250, 130)
        self.two_labels[1].move(550, 130)

        self.four_labels = [QLabel(self), QLabel(self), QLabel(self), QLabel(self)]
        for label in self.four_labels:
            label.setScaledContents(True)
            label.setFixedSize(300, 200)
        self.four_labels[0].move(250, 130)
        self.four_labels[1].move(550, 130)
        self.four_labels[2].move(250, 330)
        self.four_labels[3].move(550, 330)
        
        self.search_input_front = QLineEdit(self)
        self.search_input_front.move(10, 800)
        self.search_input_front.setPlaceholderText("Search by front")
        self.search_input_front.textChanged.connect(self.search_images)

        self.search_input_back = QLineEdit(self)
        self.search_input_back.setPlaceholderText("Search by back")
        self.search_input_back.move(10, 900)
        self.search_input_back.textChanged.connect(self.search_images)

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
    
    def search_images(self):
        query_front = self.search_input_front.text().lower()
        query_back = self.search_input_back.text().lower()
        self.search_query = query_front
        self.search_query_end = query_back

        self.load_image_paths()
        filtered_paths = [path for path in self.image_paths if query_front in os.path.basename(path).lower() and query_back in os.path.basename(path).lower()]
        self.image_list.clear()
        self.image_list.addItems(filtered_paths)
    
    def display_image(self, item):
        image_path = item.text()
        pixmap = QPixmap(image_path)
        self.one_label.setPixmap(pixmap)
        for label in self.two_labels + self.four_labels:
            label.hide()
    
    def add_image(self):
        selected_item = self.image_list.currentItem()
        if selected_item:
            print(f"Loading image from: {selected_item.text()}")  # Add this line
            self.selected_images.append(QPixmap(selected_item.text()))
            self.display_images()
        
    def display_images(self):
        if self.split_mode == 1:
            # Display the last selected image in one_label
            if self.selected_images:
                self.one_label.setPixmap(self.selected_images[0])
            else:
                self.one_label.clear()
        elif self.split_mode == 2:
            # Display the first two selected images in two_labels
            for i, label in enumerate(self.two_labels):
                if i < len(self.selected_images):
                    label.setPixmap(self.selected_images[i])
                else:
                    label.clear()
        elif self.split_mode == 4:
            # Display the first four selected images in four_labels
            for i, label in enumerate(self.four_labels):
                if i < len(self.selected_images):
                    label.setPixmap(self.selected_images[i])
                else:
                    label.clear()
                    
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
    def show_one_label(self):
        self.one_label.show()
        for label in self.two_labels + self.four_labels:
            label.clear()

    def show_two_labels(self):
        for label in self.two_labels:
            label.show()
        self.one_label.clear()
        for label in self.four_labels:
            label.clear()

    def show_four_labels(self):
        for label in self.four_labels:
            label.show()
        self.one_label.clear()
        for label in self.two_labels:
            label.clear()

    def set_selection(self, split_mode):
        self.split_mode = split_mode

        if split_mode == 1:
            self.show_one_label()
        elif split_mode == 2:
            self.show_two_labels()
        elif split_mode == 4:
            self.show_four_labels()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageViewer()
    window.show()
    sys.exit(app.exec_())
