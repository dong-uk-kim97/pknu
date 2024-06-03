# -*- coding: utf-8 -*-

import sys
import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QListWidget, QSplitter, QMessageBox, QFileDialog, QTextEdit, QHBoxLayout, QSizePolicy, QPixmap, QImage
from PyQt5.QtCore import Qt
from ftplib import FTP


class FTP_Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('FTP 브라우저')
        self.resize(1920, 1080)

        # 파일 목록 화면 UI
        self.file_list_widget = QListWidget()
        self.file_list_widget.setDragEnabled(True)
        self.file_list_widget.itemDoubleClicked.connect(self.display_image)

        # 파일 내용 화면 UI
        self.image_label = QLabel()
        self.image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.image_label.setAlignment(Qt.AlignCenter)

        # 검색 UI
        self.search_line_edit = QLineEdit()
        self.search_button = QPushButton('검색')
        self.search_button.clicked.connect(self.search_file)

        # 파일 탐색 화면 UI
        self.file_explore_widget = QSplitter(Qt.Horizontal)
        self.file_explore_widget.addWidget(self.file_list_widget)
        self.file_explore_widget.addWidget(self.image_label)

        # 파일 분할 화면 설정
        self.file_explore_widget.setSizes([960, 960])

        # 메인 레이아웃 설정
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.file_explore_widget)
        main_layout.addWidget(self.search_line_edit)
        main_layout.addWidget(self.search_button)

        # 단추 추가
        button_layout = QHBoxLayout()
        self.show_button = QPushButton('1개 보기')
        self.show_button.clicked.connect(self.show_one_image)
        self.show_button2 = QPushButton('2개 보기')
        self.show_button2.clicked.connect(self.show_two_images)
        self.show_button4 = QPushButton('4개 보기')
        self.show_button4.clicked.connect(self.show_four_images)
        button_layout.addWidget(self.show_button)
        button_layout.addWidget(self.show_button2)
        button_layout.addWidget(self.show_button4)
        main_layout.addLayout(button_layout)

        # 메인 윈도우 설정
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def search_file(self):
        """
        FTP 목록 위젯에서 검색 라인 편집에 입력된 텍스트를 기준으로 파일을 검색합니다.

        이 함수는 검색 라인 편집에서 텍스트를 검색하고, FTP 목록 위젯에서 해당 텍스트를 포함하는 아이템을 찾습니다.
        찾은 아이템이 있으면 첫 번째 아이템을 선택하고, 아이템이 없으면 경고 메시지를 표시합니다.
        """
        # 검색 라인 편집에서 텍스트를 검색합니다
        search_text = self.search_line_edit.text()

        # FTP 목록 위젯에서 검색 텍스트를 포함하는 아이템을 찾습니다
        files = self.file_list_widget.findItems(search_text, Qt.MatchContains)

        # 아이템이 있으면 첫 번째 아이템을 선택합니다
        if files:
            self.file_list_widget.setCurrentItem(files[0])
        else:
            # 아이템이 없으면 경고 메시지를 표시합니다
            QMessageBox.warning(self, '검색 결과', '검색 결과가 없습니다.')
            QMessageBox.warning(self, '검색 결과', '검색 결과가 없습니다.')

    def display_image(self, item):
        """
        FTP 서버에서 이미지를 다운로드하고, 이미지를 크기를 조정하고, 이미지 레이블에 표시합니다.

        Args:
            item (QListWidgetItem): 표시할 이미지를 나타내는 아이템입니다.
        """
        while True:
            try:
                # FTP 서버에 연결하고, 이미지를 다운로드합니다
                with FTP('ftp.nps.edu') as ftp:
                    ftp.login()
                    ftp.cwd('/pub/data/satellite/landsat_8/')
                    file_path = ftp.pwd() + '/' + item.text()
                    ftp.retrbinary('RETR ' + item.text(), open(item.text(), 'wb').write)
                break
            except:
                pass
        
        # 이미지를 읽고, 크기를 조정하고, 이미지 레이블에 표시합니다
        image = cv2.imread(item.text())
        height, width, channel = image.shape
        scaled_image = cv2.resize(image, (int(width/2), int(height/2)))
        self.image_label.setPixmap(QPixmap.fromImage(QImage(item.text(), QImage.Format_RGB888)))
        self.image_label.update()

    def show_one_image(self):
        self.display_image(self.file_list_widget.currentItem())

    def show_two_images(self):
        item1 = self.file_list_widget.currentItem()
        item2 = self.file_list_widget.item(self.file_list_widget.currentRow()+1)
        self.display_image(item1)
        self.display_image(item2)

    def show_four_images(self):
        item1 = self.file_list_widget.currentItem()
        item2 = self.file_list_widget.item(self.file_list_widget.currentRow()+1)
        item3 = self.file_list_widget.item(self.file_list_widget.currentRow()+2)
        item4 = self.file_list_widget.item(self.file_list_widget.currentRow()+3)
        self.display_image(item1)
        self.display_image(item2)
        self.display_image(item3)
        self.display_image(item4)

