from PyQt5 import QtCore, QtGui, QtWidgets
import configparser
import sys
from PyQt5.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(613, 740)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        #아이디 입력창
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(200, 330, 250, 31))
        self.lineEdit.setObjectName("lineEdit")
       

        #비밀번호 입력창
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(200, 400, 250, 31))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_2.returnPressed.connect(self.open)  # 엔터 눌렀을 때 open 함수로 가
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password) #비번 안보이게

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(150,330, 56, 12))
        self.label.setObjectName("label")
        

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(150,400, 56, 12))
        self.label_2.setObjectName("label_2")

        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(200, 500, 100, 100))
        self.label_3.setObjectName("label_3")
        
        self.lineEdit.raise_()
        self.lineEdit_2.raise_()
        self.label.raise_()
        self.label_2.raise_()
        self.label_3.raise_()
       
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def open(self): 
        self.label_3.setText("FirstClick") 
        config = configparser.ConfigParser()
        config.read("ai.ini")   
        pid = config['user']['id']         
        ppw = config['user']['pw']
        text = self.lineEdit.text()    
        text2 = self.lineEdit_2.text()  

        if text == pid and text2 == ppw:  
           self.label_3.setText("open") 

        else :
           self.label_3.setText("틀렸습니다") 


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.lineEdit.setText(_translate("MainWindow", ""))
        self.lineEdit_2.setText(_translate("MainWindow", ""))
        self.label.setText(_translate("MainWindow", "ID"))
        self.label_2.setText(_translate("MainWindow", "PW"))
        self.label_3.setText(_translate("MainWindow", ""))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())




