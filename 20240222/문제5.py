import cv2
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(613, 740)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        #로그인 창 버튼
        self.pushButton_1 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_1.setGeometry(QtCore.QRect(240, 540, 111, 31))
        self.pushButton_1.setObjectName("pushButton_1")
        self.pushButton_1.clicked.connect(self.open)
        self.pushButton_1.raise_()
        self.pushButton_1.setText('Push')

        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(240, 340, 111, 31))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.stop1)
        self.pushButton_2.raise_()
        self.pushButton_2.setText('close')
        
        self.stop = 0
        
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def open(self): 
        capture = cv2.VideoCapture('./an.mp4')
        while cv2.waitKey(20) <0:
            ret, frame = capture.read()
            if ret:    
                cv2.imshow('an', frame)
            if self.stop==1:
                self.stop=0
                break

        capture.release()
        cv2.destroyAllWindows()
        
    def stop1(self):
        self.stop=1

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        # self.pushButton_1.setText(_translate("MainWindow", "이미지"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())