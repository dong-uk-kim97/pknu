import shutil
import sys
import time
import cv2
import os
import time
import subprocess
import threading
import socket
import datetime
import webbrowser
import configparser
import sqlite3
import natsort
import glob

#from datetime import timedelta
#from datetime import datetime
import numpy as np
#from pywinusb import this
#import pywinusb
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QPixmap, QImage, QPalette
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QListWidget, QMessageBox, QLineEdit, QTextEdit
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from openpyxl import load_workbook
from PyQt5.QtMultimedia import QMediaPlaylist, QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl, QObject, pyqtSignal, pyqtSlot
from PyQt5.QtCore import QDir, Qt, QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
        QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget, QTabWidget, QHeaderView)
from PyQt5.QtWidgets import QMainWindow,QWidget, QPushButton, QAction
from PyQt5.QtGui import QIcon


sellect = 0
state = 0

ch1_w = 810
ch1_h = 650
ch2_w = 810
ch2_h = 650
ch3_w = 810
ch3_h = 650
ch4_w = 810
ch4_h = 650
ch5_w = 810
ch5_h = 650
ch6_w = 810
ch6_h = 650
ch7_w = 810
ch7_h = 650
ch8_w = 810
ch8_h = 650
ch9_w = 810
ch9_h = 650
ch10_w = 810
ch10_h = 650
ch11_w = 810
ch11_h = 650
ch12_w = 810
ch12_h = 650

ch13_w = 810
ch13_h = 650
ch14_w = 810
ch14_h = 650
ch15_w = 810
ch15_h = 650
ch16_w = 810
ch16_h = 650
#ch1_w = 3255
#ch1_h = 1830


sellect_page = 0
view_stop = 0

sellect_deep = 0
sellect_deep_image = 0

view_name1 = ''
view_name2 = ''
view_name3 = ''
view_name4 = ''
view_name5 = ''
view_name6 = ''
view_name7 = ''
view_name8 = ''
view_name9 = ''
view_name10 = ''
view_name11 = ''
view_name12 = ''

class three(QtWidgets.QWidget):
    """서브 윈도우"""
    qss2 = """
        QWidget {
            color: #FFFF00;
            background: #000020;
        }
        QWidget#windowTitle {
            color: #FF0000;
            background: #333;
        }
        QWidget#windowTitle QLabel {
            color: #FF0000;
            background: #333;
        }
    """
    def __init__(self):
        super().__init__()
        self.setStyleSheet(self.qss2)
        self.title = 'Device_SAVE'
        self.left = 650
        self.top = 650
        self.width = 1400
        self.height = 684
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.pushButton = QPushButton(self)
        #self.pushButton.setGeometry(QtCore.QRect(1050, 580, 111, 41))
        self.pushButton.setGeometry(QtCore.QRect(1185, 580, 111, 41))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("selection-background-color: rgb(39, 255, 255);\n"
                                      "border-style: solid; border-width: 2px; border-color: #ffffff; \n"
                                      "color : white;\n"
                                      "")
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setText("SAVE")
        self.pushButton.clicked.connect(self.btn_clicked)


        self.pushButton_3 = QPushButton(self)
        self.pushButton_3.setGeometry(QtCore.QRect(1229, 100, 70, 25))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setStyleSheet("selection-background-color: rgb(39, 255, 255);\n"
                                        "border-style: solid; border-width: 2px; border-color: #ffffff; \n"
                                        "color : white;\n"
                                        "")
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.setText("READ")
        self.pushButton_3.clicked.connect(self.btn_clicked_2)

        # self.label100 = QLabel(self)
        # self.label100.setGeometry(90,810,500,90)
        # self.label100.setStyleSheet("background-color : rgba(255,255,50,0);"
        #                             "color : white")
        # self.label100.setFont(QtGui.QFont("HY견고딕B", 12))
        # self.label100.setText("CAR")

        self.label = QLabel(self)
        self.label.setGeometry(40, 130, 60, 31)
        #font = QtGui.QFont()
        #font.setPointSize(12)
        #self.label.setFont(font)
        self.label.setFont(QtGui.QFont("HY견고딕B", 12))
        self.label.setStyleSheet("background-color : rgba(255,255,50,0);"
                                    "color : white")
        #self.label.setStyleSheet("color: white;")
        self.label.setLineWidth(2)
        self.label.setObjectName("label")
        self.label.setText("* 장비명")

        self.textEdit = QTextEdit(self)
        self.textEdit.setGeometry(QtCore.QRect(120, 130, 231, 31))
        self.textEdit.setAutoFillBackground(False)
        self.textEdit.setStyleSheet("background-color: rgb(22, 22, 22); color : white")
        self.textEdit.setObjectName("textEdit")
        #self.textEdit.setValidator(QIntValidator(1,255,self))

        self.textEdit_2 = QTextEdit(self)
        self.textEdit_2.setGeometry(QtCore.QRect(120, 230, 231, 31))
        self.textEdit_2.setStyleSheet("background-color: rgb(22, 22, 22); color : white")
        self.textEdit_2.setObjectName("textEdit_2")
        #self.textEdit.setValidator(QIntValidator(1, 255, self))

        self.label_2 = QLabel(self)
        self.label_2.setGeometry(QtCore.QRect(70, 230, 40, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: white;")
        self.label_2.setLineWidth(2)
        self.label_2.setObjectName("label_2")
        self.label_2.setText("포트")

        self.textEdit_3 = QTextEdit(self)
        self.textEdit_3.setGeometry(QtCore.QRect(120, 280, 231, 31))
        self.textEdit_3.setAutoFillBackground(False)
        self.textEdit_3.setStyleSheet("background-color: rgb(22, 22, 22); color : white")
        self.textEdit_3.setObjectName("textEdit_3")

        self.label_3 = QLabel(self)
        self.label_3.setGeometry(QtCore.QRect(40, 280, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("color: white;")
        self.label_3.setLineWidth(2)
        self.label_3.setObjectName("label_3")
        self.label_3.setText("고유번호는 순서대로 작성해주세요:")

        self.label_4 = QLabel(self)
        self.label_4.setGeometry(QtCore.QRect(40, 330, 61, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color: white;")
        self.label_4.setLineWidth(2)
        self.label_4.setObjectName("label_4")
        self.label_4.setText("Website")

        self.textEdit_4 = QTextEdit(self)
        self.textEdit_4.setGeometry(QtCore.QRect(120, 330, 231, 31))
        self.textEdit_4.setStyleSheet("background-color: rgb(22, 22, 22); color : white")
        self.textEdit_4.setObjectName("textEdit_4")

        self.textEdit_5 = QTextEdit(self)
        self.textEdit_5.setGeometry(QtCore.QRect(120, 180, 231, 31))
        self.textEdit_5.setAutoFillBackground(False)
        self.textEdit_5.setStyleSheet("background-color: rgb(22, 22, 22); color : white")
        self.textEdit_5.setObjectName("textEdit_5")

        self.label_5 = QLabel(self)
        self.label_5.setGeometry(QtCore.QRect(80, 180, 21, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("color: white;")
        self.label_5.setLineWidth(2)
        self.label_5.setObjectName("label_5")
        self.label_5.setText("*IP")


        self.label_6 = QLabel(self)
        self.label_6.setGeometry(QtCore.QRect(50, 380, 51, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("color: white;")
        self.label_6.setLineWidth(2)
        self.label_6.setObjectName("label_6")
        self.label_6.setText("제조사")

        self.textEdit_6 = QTextEdit(self)
        self.textEdit_6.setGeometry(QtCore.QRect(120, 430, 231, 31))
        self.textEdit_6.setStyleSheet("background-color: rgb(22, 22, 22); color : white")
        self.textEdit_6.setObjectName("textEdit_6")

        self.label_7 = QLabel(self)
        self.label_7.setGeometry(QtCore.QRect(70, 430, 31, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_7.setFont(font)
        self.label_7.setStyleSheet("color: white;")
        self.label_7.setLineWidth(2)
        self.label_7.setObjectName("label_7")
        self.label_7.setText("모델")

        self.textEdit_7 = QTextEdit(self)
        self.textEdit_7.setGeometry(QtCore.QRect(120, 380, 231, 31))
        self.textEdit_7.setAutoFillBackground(False)
        self.textEdit_7.setStyleSheet("background-color: rgb(22, 22, 22); color : white")
        self.textEdit_7.setObjectName("textEdit_7")

        self.label_8 = QLabel(self)
        self.label_8.setGeometry(QtCore.QRect(20, 480, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_8.setFont(font)
        self.label_8.setStyleSheet("color: white;")
        self.label_8.setLineWidth(2)
        self.label_8.setObjectName("label_8")
        self.label_8.setText("이벤트처리")

        self.textEdit_8 = QTextEdit(self)
        self.textEdit_8.setGeometry(QtCore.QRect(120, 480, 231, 31))
        self.textEdit_8.setStyleSheet("background-color: rgb(22, 22, 22); color : white")
        self.textEdit_8.setObjectName("textEdit_8")

        self.label_9 = QLabel(self)
        self.label_9.setGeometry(QtCore.QRect(30, 30, 790, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_9.setFont(font)
        self.label_9.setStyleSheet("color: white;")
        self.label_9.setLineWidth(2)
        self.label_9.setObjectName("label_9")
        self.label_9.setText("*는 필수항목으로 반드시 입력해주시기 바랍니다.")

        self.tableWidget = QTableWidget(self)
        self.tableWidget.setGeometry(QtCore.QRect(450, 130, 850, 381))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)

        #self.label_11 = QLabel(self)
        #self.label_11.setGeometry(QtCore.QRect(120, 30, 301, 31))
        #self.label_11.setObjectName("label_11")
        #self.label_11.setText("10")

    def btn_clicked_2(self):
        reply = QMessageBox.question(self, 'Message', '데이터를 읽어 오시겠습니까>?',
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            #event.accept()
            self.tableWidget.setColumnCount(8)
            self.tableWidget.setRowCount(10000)
            self.tableWidget.setHorizontalHeaderLabels(['장비명', "IP", "포트", "고유번호", "WebSite", "제조사", "모델", "이벤트처리"])
            self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.tableWidget.setStyleSheet("gridline-color: white; border: 0px solid; color:white")
            # con = sqlite3.connect('First.db')
            self.pushButton_3.setStyleSheet("background-color: red;\n"
                                            "color: #FF5733; border-style: solid; border-width: 1px; border-color: #FFC300;  \n"
                                            "color : white;\n"
                                            "")
            conn = sqlite3.connect("First.db", isolation_level=None)
            c = conn.cursor()
            c.execute("SELECT * FROM 장비관리")
            result = c.fetchall()
            stylesheet = "::section{Background-color:rgb(50,1,1);border-radius:14px;}"
            self.tableWidget.verticalHeader().setStyleSheet(stylesheet)  # 세로
            self.tableWidget.horizontalHeader().setStyleSheet(stylesheet)  # 가로
            # for j in range(self.tableWidget.rowCount()):
            # result_1 = result[j]
            cj = 0
            for j in result:
                # print(j)
                # for i in range(self.tableWidget.columnCount()):
                ci = 0
                for i in j:
                    # print(i)
                    self.tableWidget.setItem(cj, ci, QTableWidgetItem(str(i)))
                    # self.tableWidget.setItem(j, i, str(result_1[i]))
                    # print("result=",result_1[i])
                    # print(j,i)
                    if ci > 7:
                        ci = 0
                        break
                    ci += 1
                if cj > 10000:
                    break
                cj += 1
                # print(result)
            conn.commit()
        else:
            return


    def btn_clicked(self):
        global view_name1
        reply = QMessageBox.question(self, 'Message', '데이터를 저장하시겠습니까?',
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            # self.tx = self.textEdit.setText('dkfjdkfjdkf')
            self.tx = self.textEdit.toPlainText()
            self.tx1 = self.textEdit_5.toPlainText()
            print("self.tx=", self.tx)
            if not self.tx :
                QMessageBox.question(self, 'Message', '장비명 데이터가 입력되지 않았습니다. 입력을 해주세요',
                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            elif not self.tx1:
                QMessageBox.question(self, 'Message', 'IP 데이터가 입력되지 않았습니다. 입력을 해주세요',
                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            else:
                self.tx = self.textEdit.toPlainText()
                tx_len = len(self.tx)
                if tx_len > 20:
                    QMessageBox.question(self, 'Message', '입력 수가 초과되었습니다. 다시입력해주세요',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

                self.tx1 = self.textEdit_5.toPlainText()
                tx1_len = len(self.tx1)
                if tx1_len > 20:
                    QMessageBox.question(self, 'Message', '입력 수가 초과되었습니다. 다시입력해주세요',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

                self.tx2 = self.textEdit_2.toPlainText()
                tx2_len = len(self.tx2)
                if tx2_len > 20:
                    QMessageBox.question(self, 'Message', '입력 수가 초과되었습니다. 다시입력해주세요',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

                self.tx3 = self.textEdit_3.toPlainText()
                tx3_len = len(self.tx3)
                if tx3_len > 20:
                    QMessageBox.question(self, 'Message', '입력 수가 초과되었습니다. 다시입력해주세요',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

                self.tx4 = self.textEdit_4.toPlainText()
                tx4_len = len(self.tx4)
                if tx4_len > 20:
                    QMessageBox.question(self, 'Message', '입력 수가 초과되었습니다. 다시입력해주세요',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                self.tx5 = self.textEdit_7.toPlainText()
                tx5_len = len(self.tx5)
                if tx5_len > 20:
                    QMessageBox.question(self, 'Message', '입력 수가 초과되었습니다. 다시입력해주세요',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                self.tx6 = self.textEdit_6.toPlainText()
                tx6_len = len(self.tx6)
                if tx6_len > 20:
                    QMessageBox.question(self, 'Message', '입력 수가 초과되었습니다. 다시입력해주세요',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                self.tx7 = self.textEdit_8.toPlainText()
                tx7_len = len(self.tx7)
                if tx7_len > 20:
                    QMessageBox.question(self, 'Message', '입력 수가 초과되었습니다. 다시입력해주세요',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if tx_len < 20 and tx1_len < 20 and tx2_len <20 and tx3_len <20 and tx4_len <20 and tx5_len <20 and tx6_len <20 and tx7_len <20:
                    conn = sqlite3.connect("First.db", isolation_level=None)
                    c = conn.cursor()
                    c.execute("INSERT INTO 장비관리 ('장비명', 'IP', '웹 포트', '고유번호', 'WebSite', '제조사', '모델', '이벤트처리') VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                        (self.tx, self.tx1, self.tx2, self.tx3, self.tx4, self.tx5, self.tx6, self.tx7))
                    conn.commit()
                else :
                    QMessageBox.question(self, 'Message', '입력 수가 초과되었습니다. 처음부터 다시입력해주세요',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        else:
            return

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
PWcount = 0
fire = 0

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = three()
    ex.show()
    sys.exit(app.exec_())