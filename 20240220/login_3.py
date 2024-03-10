import configparser
import time
import cv2
import os
import socket
import argparse
import threading
import sqlite3
import ftplib
import glob
from datetime import datetime

from threading import Thread
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class SubWindow(QtWidgets.QWidget):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800,600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, 800,600))
        self.label.setObjectName("label")
        # self.label.setPixmap(QtGui.QPixmap("login.png"))

        self.lineEdit_1 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_1.setGeometry(QtCore.QRect(75, 610, 80, 20))
        self.lineEdit_1.setObjectName("lineEdit_1")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(175, 610, 270, 20))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_2.setText("rtsp://210.99.70.120:1935/live/cctv001.stream")

        self.btn1 = QPushButton(self.centralwidget)
        self.btn1.setGeometry(460, 610, 50, 20)
        self.btn1.setObjectName("PushButton1")
        self.btn1.clicked.connect(self.save)
        self.btn1.setText("Save")

        self.btn6 = QPushButton(self.centralwidget)
        self.btn6.setGeometry(204, 684, 193, 80)
        self.btn6.setObjectName("PushButton6")
        self.btn6.clicked.connect(self.quit)
        # self.btn6.setStyleSheet("background-color: transparent;")

        self.tableWidget = QTableWidget(self)
        self.tableWidget.setGeometry(QtCore.QRect(55, 55, 445, 600))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)

    def save(self):
        number1 = self.lineEdit_1.text()
        route1 = self.lineEdit_2.text()
        conn = sqlite3.connect("cctv.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO cctv1 Values('" + number1 + "','" + route1 + "')")
        conn.commit()
        conn.close()
    
    def quit(self):
        quit()
        

class Ui_MainWindow(QtWidgets.QWidget):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1920,1080)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, 1920,1080))
        self.label.setObjectName("label")
        self.label.setPixmap(QtGui.QPixmap("cctv.jpg"))
        
        self.label_1 = QtWidgets.QLabel(self.centralwidget)
        self.label_1.setGeometry(QtCore.QRect(65, 145, 270, 180))
        self.label_1.setObjectName("label_1")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(465, 145, 270, 180))
        self.label_2.setObjectName("label_2")      
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(65, 460, 270, 180))
        self.label_3.setObjectName("label_3")  
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(465, 460, 270, 180))
        self.label_4.setObjectName("label_4") 

        self.lineEdit_1 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_1.setGeometry(QtCore.QRect(160, 340, 80, 20))
        self.lineEdit_1.setObjectName("lineEdit_1")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(560, 340, 80, 20))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_3.setGeometry(QtCore.QRect(160, 655, 80, 20))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_4 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_4.setGeometry(QtCore.QRect(560, 655, 80, 20))
        self.lineEdit_4.setObjectName("lineEdit_4")

        self.btn1 = QPushButton(self.centralwidget)
        self.btn1.setGeometry(150, 40, 100, 100)
        self.btn1.setObjectName("PushButton1")
        # self.btn1.clicked.connect(self.th2)
        self.btn1.setStyleSheet("background-color: transparent;")

        self.btn6 = QPushButton(self.centralwidget)
        self.btn6.setGeometry(1467,995,173,45)
        self.btn6.setObjectName("PushButton6")
        self.btn6.clicked.connect(self.exit)
        self.btn6.setText('DB 저장')
        self.btn6.setStyleSheet("background-color: transparent;")

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.MainWindow = MainWindow    
        self.MainWindow.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.CustomizeWindowHint | QtCore.Qt.FramelessWindowHint)

        self.th1 = Thread(self)
        self.th1.changePixmap.connect(self.label_1.setPixmap)
        self.th2 = Thread2(self)
        self.th2.changePixmap.connect(self.label_2.setPixmap)
        self.th3 = Thread3(self)
        self.th3.changePixmap.connect(self.label_3.setPixmap)
        self.th4 = Thread4(self)
        self.th4.changePixmap.connect(self.label_4.setPixmap)
        self.th5 = Thread5(self)
        self.th6 = Thread6(self)
        self.th7 = Thread7(self)
        self.th8 = Thread8(self)

    def exit(self):
        if self.lineEdit_1.text() == self.lineEdit_2.text() == self.lineEdit_3.text() == self.lineEdit_4.text() == "":
            self.window = QtWidgets.QWidget()
            self.ui = SubWindow()
            self.ui.setupUi(self.window)
            self.window.show()

        else:
            global aaa
            global bbb
            global ccc
            global ddd
            global xxx
            global yyy
            global zzz
            global vvv

            xxx = self.lineEdit_1.text()
            yyy = self.lineEdit_2.text()
            zzz = self.lineEdit_3.text()
            vvv = self.lineEdit_4.text()
            conn = sqlite3.connect("cctv2.db")
            cur = conn.cursor()
            cur.execute("SELECT RTSP FROM cctv WHERE number = '" + str(self.lineEdit_1.text()) + "'")
            result1 = str(cur.fetchone())
            aaa = result1[2:-3]
            cur.execute("SELECT RTSP FROM cctv WHERE number = '" + str(self.lineEdit_2.text()) + "'")
            result2 = str(cur.fetchone())
            bbb = result2[2:-3]
            cur.execute("SELECT RTSP FROM cctv WHERE number = '" + str(self.lineEdit_3.text()) + "'")
            result3 = str(cur.fetchone())
            ccc = result3[2:-3]
            cur.execute("SELECT RTSP FROM cctv WHERE number = '" + str(self.lineEdit_4.text()) + "'")
            result4 = str(cur.fetchone())
            ddd = result4[2:-3]
            conn.commit()
            conn.close()

            self.th1.start()
            self.th2.start()
            self.th3.start()
            self.th4.start()
            self.th5.start()
            self.th6.start()
            self.th7.start()
            self.th8.start()


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

class Thread(QThread):
    changePixmap = pyqtSignal(QPixmap)
    def __init__(self, parent=None):
        QThread.__init__(self, parent=parent)
        self.isRunning = True
    def run(self):
            cap = cv2.VideoCapture(aaa)
            if cap.isOpened() is False:
                #print("1")
                self.isRunning = False
            else :
                self.isRunning = True
            while self.isRunning:
                ret, frame = cap.read()
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                convertToQtFormat = QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0], QImage.Format_RGB888)
                convertToQtFormat = QPixmap.fromImage(convertToQtFormat)
                p = convertToQtFormat.scaled(270, 180, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)
                if not ret:
                    self.isRunning = False
                    break
            cap.release()
            cv2.destroyAllWindows()
    def resume(self):
        self.isRunning = True
    def stop(self):
        cv2.destroyAllWindows()
        self.isRunning = False

class Thread5(QThread):
    changePixmap = pyqtSignal(QPixmap)
    def __init__(self, parent=None):
        QThread.__init__(self, parent=parent)
        self.isRunning = True
    def run(self):
        global aaa
        global xxx
        conn = sqlite3.connect("cctv2.db")
        cur = conn.cursor()
        cur.execute("SELECT RTSP FROM cctv WHERE number = '" + str(xxx) + "'")
        result1 = str(cur.fetchone())
        aaa = result1[2:-3]
        cur.execute("SELECT latitude FROM cctv WHERE number = '" + str(xxx) + "'")
        result2 = str(cur.fetchone())
        whido1 = result2[2:-3]
        cur.execute("SELECT longitude FROM cctv WHERE number = '" + str(xxx) + "'")
        result3 = str(cur.fetchone())
        gyeongdo1 = result3[2:-3]
        conn.commit()
        conn.close()
        cap = cv2.VideoCapture(aaa)
        now = datetime.now()
        os.makedirs("C:\\study\\20240223\\" + now.strftime("%Y") + "\\" + now.strftime("%m") + "\\" + now.strftime("%d") + "\\" + now.strftime("%H"), exist_ok=True)
        filename = "C:\\study\\20240223\\" + now.strftime("%Y") + "\\" + now.strftime("%m") + "\\" + now.strftime("%d") + "\\" + now.strftime("%H") + "\\" + "Busan_Namgu_" + whido1 + "_" + gyeongdo1 + "_CCNDCCTV_A.avi"
        #print(cap)
        conn = sqlite3.connect("cctv3.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO cctv Values('" + filename + "','" + filename[-14:] + "')")
        conn.commit()
        conn.close()
        if not cap.isOpened():
            cap.release()
            print(cap)
            pass
        #fps = cap.get(cv2.CAP_PROP_FPS)
        fourcc = cv2.VideoWriter_fourcc(*'DIVX')
        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        print(filename)
        out = cv2.VideoWriter(filename, fourcc,  20.0, (int(width), int(height)))
        while True:
            self.ret, self.frame = cap.read()
            if self.ret:
                out.write(self.frame)
                print("녹화중")
            else:
                cap.release()
                # print('ret=',self.ret)
                pass
    def resume(self):
        self.isRunning = True
    def stop(self):
        cv2.destroyAllWindows()
        self.isRunning = False


class Thread2(QThread):
    changePixmap = pyqtSignal(QPixmap)
    def __init__(self, parent=None):
        QThread.__init__(self, parent=parent)
        self.isRunning = True
    def run(self):
            cap = cv2.VideoCapture(bbb)
            if cap.isOpened() is False:
                #print("1")
                self.isRunning = False
            else :
                self.isRunning = True
            while self.isRunning:
                ret, frame = cap.read()
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                convertToQtFormat = QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0], QImage.Format_RGB888)
                convertToQtFormat = QPixmap.fromImage(convertToQtFormat)
                p = convertToQtFormat.scaled(270, 180, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)
                if not ret:
                    self.isRunning = False
                    break
            cap.release()
            cv2.destroyAllWindows()
    def resume(self):
        self.isRunning = True
    def stop(self):
        cv2.destroyAllWindows()
        self.isRunning = False

class Thread6(QThread):
    changePixmap = pyqtSignal(QPixmap)
    def __init__(self, parent=None):
        QThread.__init__(self, parent=parent)
        self.isRunning = True
    def run(self):
        global bbb
        global yyy
        conn = sqlite3.connect("cctv2.db")
        cur = conn.cursor()
        cur.execute("SELECT RTSP FROM cctv WHERE number = '" + str(yyy) + "'")
        result1 = str(cur.fetchone())
        aaa = result1[2:-3]
        cur.execute("SELECT latitude FROM cctv WHERE number = '" + str(yyy) + "'")
        result2 = str(cur.fetchone())
        whido1 = result2[2:-3]
        cur.execute("SELECT longitude FROM cctv WHERE number = '" + str(yyy) + "'")
        result3 = str(cur.fetchone())
        gyeongdo1 = result3[2:-3]
        conn.commit()
        conn.close()
        cap = cv2.VideoCapture(bbb)
        now = datetime.now()
        os.makedirs("C:\\study\\20240223\\" + now.strftime("%Y") + "\\" + now.strftime("%m") + "\\" + now.strftime("%d") + "\\" + now.strftime("%H"), exist_ok=True)
        filename = "C:\\study\\20240223\\" + now.strftime("%Y") + "\\" + now.strftime("%m") + "\\" + now.strftime("%d") + "\\" + now.strftime("%H") + "\\" + "Busan_Namgu_" + whido1 + "_" + gyeongdo1 + "_CCNDCCTV_B.avi"
        #print(cap)
        conn = sqlite3.connect("cctv3.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO cctv Values('" + filename + "','" + filename[-14:] + "')")
        conn.commit()
        conn.close()
        if not cap.isOpened():
            cap.release()
            print(cap)
            pass
        #fps = cap.get(cv2.CAP_PROP_FPS)
        fourcc = cv2.VideoWriter_fourcc(*'DIVX')
        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        print(filename)
        out = cv2.VideoWriter(filename, fourcc,  20.0, (int(width), int(height)))
        while True:
            self.ret, self.frame = cap.read()
            if self.ret:
                out.write(self.frame)
                print("녹화중")
            else:
                cap.release()
                # print('ret=',self.ret)
                pass
    def resume(self):
        self.isRunning = True
    def stop(self):
        cv2.destroyAllWindows()
        self.isRunning = False


class Thread3(QThread):
    changePixmap = pyqtSignal(QPixmap)
    def __init__(self, parent=None):
        QThread.__init__(self, parent=parent)
        self.isRunning = True
    def run(self):
            cap = cv2.VideoCapture(ccc)
            if cap.isOpened() is False:
                #print("1")
                self.isRunning = False
            else :
                self.isRunning = True
            while self.isRunning:
                ret, frame = cap.read()
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                convertToQtFormat = QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0], QImage.Format_RGB888)
                convertToQtFormat = QPixmap.fromImage(convertToQtFormat)
                p = convertToQtFormat.scaled(270, 180, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)
                if not ret:
                    self.isRunning = False
                    break
            cap.release()
            cv2.destroyAllWindows()
    def resume(self):
        self.isRunning = True
    def stop(self):
        cv2.destroyAllWindows()
        self.isRunning = False

class Thread7(QThread):
    changePixmap = pyqtSignal(QPixmap)
    def __init__(self, parent=None):
        QThread.__init__(self, parent=parent)
        self.isRunning = True
    def run(self):
        global ccc
        global zzz
        conn = sqlite3.connect("cctv2.db")
        cur = conn.cursor()
        cur.execute("SELECT RTSP FROM cctv WHERE number = '" + str(zzz) + "'")
        result1 = str(cur.fetchone())
        aaa = result1[2:-3]
        cur.execute("SELECT latitude FROM cctv WHERE number = '" + str(zzz) + "'")
        result2 = str(cur.fetchone())
        whido1 = result2[2:-3]
        cur.execute("SELECT longitude FROM cctv WHERE number = '" + str(zzz) + "'")
        result3 = str(cur.fetchone())
        gyeongdo1 = result3[2:-3]
        conn.commit()
        conn.close()
        cap = cv2.VideoCapture(bbb)
        now = datetime.now()
        os.makedirs("C:\\study\\20240223\\" + now.strftime("%Y") + "\\" + now.strftime("%m") + "\\" + now.strftime("%d") + "\\" + now.strftime("%H"), exist_ok=True)
        filename = "C:\\study\\20240223\\" + now.strftime("%Y") + "\\" + now.strftime("%m") + "\\" + now.strftime("%d") + "\\" + now.strftime("%H") + "\\" + "Busan_Namgu_" + whido1 + "_" + gyeongdo1 + "_CCNDCCTV_C.avi"
        #print(cap)
        conn = sqlite3.connect("cctv3.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO cctv Values('" + filename + "','" + filename[-14:] + "')")
        conn.commit()
        conn.close()
        if not cap.isOpened():
            cap.release()
            print(cap)
            pass
        #fps = cap.get(cv2.CAP_PROP_FPS)
        fourcc = cv2.VideoWriter_fourcc(*'DIVX')
        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        print(filename)
        out = cv2.VideoWriter(filename, fourcc,  20.0, (int(width), int(height)))
        while True:
            self.ret, self.frame = cap.read()
            if self.ret:
                out.write(self.frame)
                print("녹화중")
            else:
                cap.release()
                # print('ret=',self.ret)
                pass
    def resume(self):
        self.isRunning = True
    def stop(self):
        cv2.destroyAllWindows()
        self.isRunning = False


class Thread4(QThread):
    changePixmap = pyqtSignal(QPixmap)
    def __init__(self, parent=None):
        QThread.__init__(self, parent=parent)
        self.isRunning = True
    def run(self):
            cap = cv2.VideoCapture(ddd)
            if cap.isOpened() is False:
                #print("1")
                self.isRunning = False
            else :
                self.isRunning = True
            while self.isRunning:
                ret, frame = cap.read()
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                convertToQtFormat = QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0], QImage.Format_RGB888)
                convertToQtFormat = QPixmap.fromImage(convertToQtFormat)
                p = convertToQtFormat.scaled(270, 180, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)
                if not ret:
                    self.isRunning = False
                    break
            cap.release()
            cv2.destroyAllWindows()
    def resume(self):
        self.isRunning = True
    def stop(self):
        cv2.destroyAllWindows()
        self.isRunning = False

class Thread8(QThread):
    changePixmap = pyqtSignal(QPixmap)
    def __init__(self, parent=None):
        QThread.__init__(self, parent=parent)
        self.isRunning = True
    def run(self):
        global ddd
        global vvv
        conn = sqlite3.connect("cctv2.db")
        cur = conn.cursor()
        cur.execute("SELECT RTSP FROM cctv WHERE number = '" + str(vvv) + "'")
        result1 = str(cur.fetchone())
        aaa = result1[2:-3]
        cur.execute("SELECT latitude FROM cctv WHERE number = '" + str(vvv) + "'")
        result2 = str(cur.fetchone())
        whido1 = result2[2:-3]
        cur.execute("SELECT longitude FROM cctv WHERE number = '" + str(vvv) + "'")
        result3 = str(cur.fetchone())
        gyeongdo1 = result3[2:-3]
        conn.commit()
        conn.close()
        cap = cv2.VideoCapture(vvv)
        now = datetime.now()
        os.makedirs("C:\\study\\20240223\\" + now.strftime("%Y") + "\\" + now.strftime("%m") + "\\" + now.strftime("%d") + "\\" + now.strftime("%H"), exist_ok=True)
        filename = "C:\\study\\20240223\\" + now.strftime("%Y") + "\\" + now.strftime("%m") + "\\" + now.strftime("%d") + "\\" + now.strftime("%H") + "\\" + "Busan_Namgu_" + whido1 + "_" + gyeongdo1 + "_CCNDCCTV_D.avi"
        #print(cap)
        conn = sqlite3.connect("cctv3.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO cctv Values('" + filename + "','" + filename[-14:] + "')")
        conn.commit()
        conn.close()
        if not cap.isOpened():
            cap.release()
            print(cap)
            pass
        #fps = cap.get(cv2.CAP_PROP_FPS)
        fourcc = cv2.VideoWriter_fourcc(*'DIVX')
        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        print(filename)
        out = cv2.VideoWriter(filename, fourcc,  20.0, (int(width), int(height)))
        while True:
            self.ret, self.frame = cap.read()
            if self.ret:
                out.write(self.frame)
                print("녹화중")
            else:
                cap.release()
                # print('ret=',self.ret)
                pass
    def resume(self):
        self.isRunning = True
    def stop(self):
        cv2.destroyAllWindows()
        self.isRunning = False


if __name__ == "__main__":
    import sys #object는 윈도의 최고 조상
    app = QtWidgets.QApplication(sys.argv) # sys.argv는 현재 작업중인.py 절대 경로를 인자로 넘겨줌
    MainWindow = QtWidgets.QMainWindow() #윈도우 UI를 연결하기 위한 상속
    ui = Ui_MainWindow() #위 클래스를 ui 변수에 넣는다 여기서 부터 클래스 개념 필요
    ui.setupUi(MainWindow) #위 QtWidgets.QMainWindows()에서 상속받아서 위 SetupUi함수 인자로 넘겨줌 즉 위젯 실행하라는 뜻
    MainWindow.show() #MainWindow를 화면에 표시
    sys.exit(app.exec_()) #무한루프


