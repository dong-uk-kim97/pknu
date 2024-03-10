# rtsp5.py
from PyQt5 import QtCore, QtGui, QtWidgets

import cv2
import os
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QImage
import sqlite3
import sys


t1 = ""
t2 = ""
t3 = ""
t4 = ""

class Ui_MainWindow(QtWidgets.QWidget):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow") #if__name__main에서 상속받아서 앞으로는 MainWindow로 사용
        MainWindow.resize(1920, 1080)
        self.centralwidget = QtWidgets.QWidget(MainWindow) #위젯 중앙을 설정을 하고 centralwidget에 MainWindow가 모두 넘겨줌(상속)
        self.centralwidget.setObjectName("centralwidget")
        
        self.MainWindow = MainWindow
        self.MainWindow.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.CustomizeWindowHint | QtCore.Qt.FramelessWindowHint)
        
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(0, 0, 1920,1080))
        self.label_3.setObjectName("label_3")
        self.label_3.setPixmap(QtGui.QPixmap("C:\\study\\20240220\\cctv.jpg"))
        
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(455, 156, 670, 293))
        self.label.setObjectName("label")
        
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(1195,157, 670, 293))
        self.label_2.setObjectName("label_2")      
                
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(455, 518, 670,293))
        self.label_4.setObjectName("label_4")
        
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(1195, 518, 670, 293))
        self.label_5.setObjectName("label_5")       

        # self.label_6 = QtWidgets.QLabel(self.centralwidget)
        # self.label_6.setGeometry(QtCore.QRect(34, 347, 227, 294))
        # self.label_6.setObjectName("label")
        
        # self.label_7 = QtWidgets.QLabel(self.centralwidget)
        # self.label_7.setGeometry(QtCore.QRect(600,997,200,50))
        # self.label_7.setObjectName('label_7')
        # self.label_7.setText('RTSP 주소를 입력하세요.')
 
 ########################################################################
        
        # self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        # self.lineEdit.setGeometry(QtCore.QRect(750, 995, 600, 50))
        # self.lineEdit.setObjectName("lineEdit")
        # # self.lineEdit.returnPressed.connect(self.input_rtsp)
        
        # self.lineEdit2 = QtWidgets.QLineEdit(self.centralwidget)
        # self.lineEdit2.setGeometry(QtCore.QRect(680, 467, 200, 20))
        # self.lineEdit2.setObjectName("lineEdit2")
        # self.lineEdit2.returnPressed.connect(self.start_thread)
        
        # self.lineEdit3 = QtWidgets.QLineEdit(self.centralwidget)
        # self.lineEdit3.setGeometry(QtCore.QRect(1440, 467, 200, 20))
        # self.lineEdit3.setObjectName("lineEdit3")
        # self.lineEdit3.returnPressed.connect(self.start_thread2)
        
        # self.lineEdit4 = QtWidgets.QLineEdit(self.centralwidget)
        # self.lineEdit4.setGeometry(QtCore.QRect(680, 825, 200, 20))
        # self.lineEdit4.setObjectName("lineEdit4")
        # self.lineEdit4.returnPressed.connect(self.start_thread3)
        
        # self.lineEdit5 = QtWidgets.QLineEdit(self.centralwidget)
        # self.lineEdit5.setGeometry(QtCore.QRect(1440, 825, 200, 20))
        # self.lineEdit5.setObjectName("lineEdit4")
        # self.lineEdit5.returnPressed.connect(self.start_thread4)

########################################################################
        self.btn = QtWidgets.QPushButton(self.centralwidget)
        self.btn.setGeometry(QtCore.QRect(1690,992,176,50))
        self.btn.setObjectName('Pushbutton')
        self.btn.setStyleSheet('border:None; font:30;')
        self.btn.clicked.connect(self.exit)
        self.btn.setText('EXIT')
        
        self.btn2 = QtWidgets.QPushButton(self.centralwidget)
        self.btn2.setGeometry(QtCore.QRect(1467,995,173,45))
        self.btn2.setObjectName('Pushbutton2')
        self.btn2.setStyleSheet('border:None; font:30;')
        self.btn2.clicked.connect(self.start_thread)
        self.btn2.setText('ENTER')

        
        # self.rtspButton1 = QtWidgets.QPushButton(self.centralwidget)
        # self.rtspButton1.setGeometry(QtCore.QRect(455, 455, 50, 20))
        # self.rtspButton1.setObjectName("rtspButton")
        # self.rtspButton1.setText("RTSP1")
        # self.rtspButton1.setStyleSheet('background-color: gray; border:none')
        # self.rtspButton1.clicked.connect(self.start_thread)
        
        # self.rtspButton2 = QtWidgets.QPushButton(self.centralwidget)
        # self.rtspButton2.setGeometry(QtCore.QRect(1196, 455, 50, 20))
        # self.rtspButton2.setObjectName("rtspButton")
        # self.rtspButton2.setText("RTSP2")
        # self.rtspButton2.setStyleSheet('background-color: gray; border:none')
        # self.rtspButton2.clicked.connect(self.start_thread2)
               
        # self.rtspButton3 = QtWidgets.QPushButton(self.centralwidget)
        # self.rtspButton3.setGeometry(QtCore.QRect(457, 817, 50, 20))
        # self.rtspButton3.setObjectName("rtspButton")
        # self.rtspButton3.setText("RTSP3")
        # self.rtspButton3.setStyleSheet('background-color: gray; border:none')
        # self.rtspButton3.clicked.connect(self.start_thread3)
        
        # self.rtspButton4 = QtWidgets.QPushButton(self.centralwidget)
        # self.rtspButton4.setGeometry(QtCore.QRect(1196, 817, 50, 20))
        # self.rtspButton4.setObjectName("rtspButton")
        # self.rtspButton4.setText("RTSP4")
        # self.rtspButton4.setStyleSheet('background-color: gray; border:none')
        # self.rtspButton4.clicked.connect(self.start_thread4)
        
 #########################################################################       
      
        MainWindow.setCentralWidget(self.centralwidget)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
########################################################################################        
    # def input_rtsp(self):
    #     self.messagebox = QtWidgets.QMessageBox()
    #     reply = QtWidgets.QMessageBox.question(self, 'Message', '정말 이게 맞습니까?',
    #                                 QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
    #     if reply == QtWidgets.QMessageBox.Yes:
    #         self.db()
    #     else:
    #         QtWidgets.QMessageBox.warning(self, "QMessageBox", "QMessageBox Warning")
       
    def start_thread(self):
        self.th = Thread(self)
        self.th.changePixmap.connect(self.label.setPixmap)
        self.th2 = Thread2(self)
        self.th2.changePixmap.connect(self.label_2.setPixmap)
        self.th3 = Thread3(self)
        self.th3.changePixmap.connect(self.label_4.setPixmap)
        self.th4 = Thread4(self)
        self.th4.changePixmap.connect(self.label_5.setPixmap)
        self.th.start()
        self.th2.start() 
        self.th3.start()   
        self.th4.start()
        print(t1,t2,t3,t4 +'입니다.')
        os.system('cd C:\\study && cd 20240220 && cd output && cd save_file26 && save_file26.exe')

    # def db(self):
    #     text=self.lineEdit.text()
    #     text2=text.split('/')
    #     text3=text2[-1].split('.')
    #     text4=text3[0]
    #     con = sqlite3.connect('rtsp.db')
    #     cur = con.cursor()
    #     cur.execute('CREATE TABLE IF NOT EXISTS Rtsp (name text, path text)')
    #     cur.execute('INSERT OR IGNORE INTO Rtsp (name, path) VALUES(?,?)',(text4,text))
    #     con.commit()
    #     con.close()

    def exit(self):
        sys.exit()
              
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        # MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        #self.label.setText(_translate("MainWindow", "ID"))
        #self.label_2.setText(_translate("MainWindow", "PW"))
###############################################################################
class Thread(QThread):
    changePixmap = pyqtSignal(QtGui.QPixmap)
    def __init__(self, parent=None):
        QThread.__init__(self, parent=parent)
        self.isRunning = True
        
    def run(self):
        global t1
        try:
            con = sqlite3.connect('rtsp.db')
            cur = con.cursor()
            cur.execute(f'SELECT path FROM Rtsp WHERE name="{t1}"')
            path = cur.fetchone()
            
            # print(path[0])
            cap = cv2.VideoCapture(path[0])
            con.close()
            if cap.isOpened() is False:
                #print("1")
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
        
class Thread2(QThread):
    changePixmap = pyqtSignal(QtGui.QPixmap)
    def __init__(self, parent=None):
        QThread.__init__(self, parent=parent)
        self.isRunning = True
        
    def run(self):
        global t2
        con = sqlite3.connect('rtsp.db')
        cur = con.cursor()
        cur.execute(f'SELECT path FROM Rtsp WHERE name="{t2}"')
        path = cur.fetchone()
        
        # print(path[0])
        cap = cv2.VideoCapture(path[0])
        con.close()
        if cap.isOpened() is False:
            #print("1")
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
        cap.release()
        cv2.destroyAllWindows()
  
    def resume(self):
        self.isRunning = True
    def stop(self):
        cv2.destroyAllWindows()
        self.isRunning = False
        
class Thread3(QThread):
    changePixmap = pyqtSignal(QtGui.QPixmap)
    def __init__(self, parent=None):
        QThread.__init__(self, parent=parent)
        self.isRunning = True
        
    def run(self):
        global t3
        con = sqlite3.connect('rtsp.db')
        cur = con.cursor()
        cur.execute(f'SELECT path FROM Rtsp WHERE name="{t3}"')
        path = cur.fetchone()
        
        cap = cv2.VideoCapture(path[0])
        con.close()
        if cap.isOpened() is False:
            #print("1")
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
        cap.release()
        cv2.destroyAllWindows()
  
    def resume(self):
        self.isRunning = True
    def stop(self):
        cv2.destroyAllWindows()
        self.isRunning = False
        
class Thread4(QThread):
    changePixmap = pyqtSignal(QtGui.QPixmap)
    def __init__(self, parent=None):
        QThread.__init__(self, parent=parent)
        super().__init__()
        self.isRunning = True
        
    def run(self):
        global t4
        con = sqlite3.connect('rtsp.db')
        cur = con.cursor()
        cur.execute(f'SELECT path FROM Rtsp WHERE name="{t4}"')
        path = cur.fetchone()
        
        # print(path[0])
        cap = cv2.VideoCapture(path[0])
        con.close()
        if cap.isOpened() is False:
            #print("1")
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
        cap.release()
        cv2.destroyAllWindows()
                
    def resume(self):
        self.isRunning = True
    def stop(self):
        cv2.destroyAllWindows()
        self.isRunning = False
        
        
class MainWindow1(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.setObjectName("MainWindow1")
        self.resize(400, 300)

        self.lineEdit1 = QtWidgets.QLineEdit(self)
        self.lineEdit1.setGeometry(QtCore.QRect(50, 20, 230, 30))
        self.lineEdit1.setObjectName("lineEdit1")
        self.lineEdit1.returnPressed.connect(self.open1)
        
        self.lineEdit2 = QtWidgets.QLineEdit(self)
        self.lineEdit2.setGeometry(QtCore.QRect(50, 70, 230, 30))
        self.lineEdit2.setObjectName("lineEdit2")
        self.lineEdit2.returnPressed.connect(self.open2)
        
        self.lineEdit3 = QtWidgets.QLineEdit(self)
        self.lineEdit3.setGeometry(QtCore.QRect(50, 120, 230, 30))
        self.lineEdit3.setObjectName("lineEdit3")
        self.lineEdit3.returnPressed.connect(self.open3)
        
        self.lineEdit4 = QtWidgets.QLineEdit(self)
        self.lineEdit4.setGeometry(QtCore.QRect(50, 170, 230, 30))
        self.lineEdit4.setObjectName("lineEdit1")
        self.lineEdit4.returnPressed.connect(self.open4)
        
        
        self.label_1 = QtWidgets.QLabel(self)
        self.label_1.setGeometry(QtCore.QRect(50, 20, 230, 30))
        self.label_1.setObjectName("label_1")
        
        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setGeometry(QtCore.QRect(50, 70, 230, 30))
        self.label_2.setObjectName("label_2")
        
        self.label_3 = QtWidgets.QLabel(self)
        self.label_3.setGeometry(QtCore.QRect(50, 120, 230, 30))
        self.label_3.setObjectName("label_3")
        
        self.label_4 = QtWidgets.QLabel(self)
        self.label_4.setGeometry(QtCore.QRect(50, 170, 230, 30))
        self.label_4.setObjectName("label_4")
        
        
  
        
    def open1(self):
        global t1
        text = self.lineEdit1.text()
        text2=text.split('/')
        text3=text2[-1].split('.')
        text4=text3[0]
        t1 = text4
        con = sqlite3.connect('rtsp.db')
        cur = con.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS Rtsp (name text, path text)')
        cur.execute('INSERT OR IGNORE INTO Rtsp (name, path) VALUES(?,?)',(text4,text))
        con.commit()
        con.close()
        self.lineEdit1.setHidden(True)
        self.label_1.setText("DB저장 완료")
        
    def open2(self):
        global t2
        text = self.lineEdit2.text()
        text2=text.split('/')
        text3=text2[-1].split('.')
        text4=text3[0]
        t2 = text4
        con = sqlite3.connect('rtsp.db')
        cur = con.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS Rtsp (name text, path text)')
        cur.execute('INSERT OR IGNORE INTO Rtsp (name, path) VALUES(?,?)',(text4,text))
        con.commit()
        con.close()
        self.lineEdit2.setHidden(True)
        self.label_2.setText("DB저장 완료")
        
    def open3(self):
        global t3
        text = self.lineEdit3.text()
        text2=text.split('/')
        text3=text2[-1].split('.')
        text4=text3[0]
        t3 = text4
        con = sqlite3.connect('rtsp.db')
        cur = con.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS Rtsp (name text, path text)')
        cur.execute('INSERT OR IGNORE INTO Rtsp (name, path) VALUES(?,?)',(text4,text))
        con.commit()
        con.close()
        self.lineEdit3.setHidden(True)
        self.label_3.setText("DB저장 완료")
        
    def open4(self):
        global t4
        text = self.lineEdit4.text()
        text2=text.split('/')
        text3=text2[-1].split('.')
        text4=text3[0]
        t4 = text4
        con = sqlite3.connect('rtsp.db')
        cur = con.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS Rtsp (name text, path text)')
        cur.execute('INSERT OR IGNORE INTO Rtsp (name, path) VALUES(?,?)',(text4,text))
        con.commit()
        con.close()
        self.lineEdit4.setHidden(True)
        self.label_4.setText("DB저장 완료") 
        self.close()      
##########################################################################################################################
if __name__ == "__main__":
    import sys #object는 윈도의 최고 조상
    app = QtWidgets.QApplication(sys.argv) # sys.argv는 현재 작업중인.py 절대 경로를 인자로 넘겨줌
    MainWindow = QtWidgets.QMainWindow() #윈도우 UI를 연결하기 위한 상속
    ui = Ui_MainWindow() #위 클래스를 ui 변수에 넣는다 여기서 부터 클래스 개념 필요
    ui.setupUi(MainWindow) #위 QtWidgets.QMainWindows()에서 상속받아서 위 SetupUi함수 인자로 넘겨줌 즉 위젯 실행하라는 뜻
    MainWindow.show()#MainWindow를 화면에 표시
    mainWindow1 = MainWindow1()
    mainWindow1.show()
    sys.exit(app.exec_()) #무한루프


