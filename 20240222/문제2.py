from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5.QtWidgets import *


class secondwindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(613, 740)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.MainWindow = MainWindow
        
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName('label')
        self.label.setText('secondwindow')
        self.label.setGeometry(250,200,200,200)



    #텍스트 편집    
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

       
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


       
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def open(self): 
        self.window = QtWidgets.QWidget()
        self.ui = secondwindow() # 두번째 창 열기
        self.ui.setupUi(self.window)
        self.window.show()
        MainWindow.hide()

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




