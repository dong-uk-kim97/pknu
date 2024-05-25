# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QListWidget, QSplitter, QMessageBox, QFileDialog, QTextEdit
from PyQt5.QtCore import Qt
from ftplib import FTP


class FTP_Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('FTP 브라우저')
        self.resize(800, 600)

        # 파일 목록 화면 UI
        self.file_list_widget = QListWidget()
        self.file_list_widget.setDragEnabled(True)

        # 파일 내용 화면 UI
        self.file_content_widget = QTextEdit()

        # 검색 UI
        self.search_line_edit = QLineEdit()
        self.search_button = QPushButton('검색')
        self.search_button.clicked.connect(self.search_file)

        # 파일 탐색 화면 UI
        self.file_explore_widget = QSplitter(Qt.Horizontal)
        self.file_explore_widget.addWidget(self.file_list_widget)
        self.file_explore_widget.addWidget(self.file_content_widget)

        # 파일 분할 화면 설정
        self.file_explore_widget.setSizes([400, 400])

        # 메인 레이아웃 설정
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.file_explore_widget)
        main_layout.addWidget(self.search_line_edit)
        main_layout.addWidget(self.search_button)

        # 메인 윈도우 설정
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def search_file(self):
        search_text = self.search_line_edit.text()
        files = self.file_list_widget.findItems(search_text, Qt.MatchContains)
        if files:
            self.file_list_widget.setCurrentItem(files[0])
        else:
            QMessageBox.warning(self, '검색 결과', '검색 결과가 없습니다.')
