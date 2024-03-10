# rtsp5.py
from PyQt5 import QtCore, QtGui, QtWidgets

import cv2
import os
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QImage
import sqlite3
import sys


class Ui_MainWindow(QtWidgets.QWidget):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow") #if__name__main에서 상속받아서 앞으로는 MainWindow로 사용
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow) #위젯 중앙을 설정을 하고 centralwidget에 MainWindow가 모두 넘겨줌(상속)
        self.centralwidget.setObjectName("centralwidget")
        
        self.MainWindow = MainWindow
        self.MainWindow.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.CustomizeWindowHint | QtCore.Qt.FramelessWindowHint)
        
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(150, 100, 500, 400))
        self.label.setObjectName("label")

        self.btn = QtWidgets.QPushButton(self.centralwidget)
        self.btn.setGeometry(QtCore.QRect(300,500,173,45))
        self.btn.setObjectName('Pushbutton')
        self.btn.clicked.connect(self.start_thread)
        self.btn.setText('ENTER')
        
        MainWindow.setCentralWidget(self.centralwidget)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
########################################################################################        

    def start_thread(self):
        self.th = Thread(self)
        self.th.changePixmap.connect(self.label.setPixmap)
        self.th.start()
    def exit(self):
        sys.exit()
              
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate

###############################################################################
class Thread(QThread):
    changePixmap = pyqtSignal(QtGui.QPixmap)
    def __init__(self, parent=None):
        QThread.__init__(self, parent=parent)
        self.isRunning = True
        
    def run(self):
        try:
            path = './an.mp4'
            cap = cv2.VideoCapture(path)
            if cap.isOpened() is False:
                self.isRunning = False
            else :
                self.isRunning = True

            while self.isRunning:
                ret, frame = cap.read()
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                convertToQtFormat = QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0], QImage.Format_RGB888)
                convertToQtFormat = QtGui.QPixmap.fromImage(convertToQtFormat)
                p = convertToQtFormat.scaled(690, 293, Qt.IgnoreAspectRatio)
                self.changePixmap.emit(p)
                if not ret:
                    self.isRunning = False
                    break
        except cv2.error as e:
            print(e)

        cap.release()
        cv2.destroyAllWindows()
  
    def resume(self):
        self.isRunning = True
    def stop(self):
        cv2.destroyAllWindows()
        self.isRunning = False
        
        
         
##########################################################################################################################
if __name__ == "__main__":
    import sys #object는 윈도의 최고 조상
    app = QtWidgets.QApplication(sys.argv) # sys.argv는 현재 작업중인.py 절대 경로를 인자로 넘겨줌
    MainWindow = QtWidgets.QMainWindow() #윈도우 UI를 연결하기 위한 상속
    ui = Ui_MainWindow() #위 클래스를 ui 변수에 넣는다 여기서 부터 클래스 개념 필요
    ui.setupUi(MainWindow) #위 QtWidgets.QMainWindows()에서 상속받아서 위 SetupUi함수 인자로 넘겨줌 즉 위젯 실행하라는 뜻
    MainWindow.show()#MainWindow를 화면에 표시
    sys.exit(app.exec_()) #무한루프


