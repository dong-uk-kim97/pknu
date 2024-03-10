from PyQt5 import QtCore, QtGui, QtWidgets
import configparser
import time
import cv2
import os
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QLabel

gcount = 0
timecount = 0

class Ui_MainWindow(QtWidgets.QWidget):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow") #if__name__main에서 상속받아서 앞으로는 MainWindow로 사용
        MainWindow.resize(541, 741)
        self.centralwidget = QtWidgets.QWidget(MainWindow) #위젯 중앙을 설정을 하고 centralwidget에 MainWindow가 모두 넘겨줌(상속)
        self.centralwidget.setObjectName("centralwidget")
        
        self.MainWindow = MainWindow
        self.MainWindow.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.CustomizeWindowHint | QtCore.Qt.FramelessWindowHint)
        
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(1, 1, 541, 741))
        self.label_3.setObjectName("label_3")
        self.label_3.setPixmap(QtGui.QPixmap("frame1.png"))
        
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(34, 32, 248, 293))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(460, 590, 56, 20))
        self.label_2.setObjectName("label_2")      
                
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(1, 350, 414, 350))
        self.label_4.setObjectName("label_4")
        self.label_4.setPixmap(QtGui.QPixmap("test.png"))
        self.label_4.setHidden(True)
        
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(285, 32, 227, 293))
        self.label_5.setObjectName("label_5")       

        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(34, 347, 227, 294))
        self.label_6.setObjectName("label")
        
        
        # self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        # self.lineEdit.setGeometry(QtCore.QRect(173, 453, 150, 20))
        # self.lineEdit.setObjectName("lineEdit")
        # self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        # self.lineEdit_2.setGeometry(QtCore.QRect(173, 506, 150, 20))
        # self.lineEdit_2.setObjectName("lineEdit_2")

        self.btn = QtWidgets.QPushButton(self.centralwidget)
        self.btn.setGeometry(QtCore.QRect(458,663,51,49))
        self.btn.setObjectName('Pushbutton')
        self.btn.setStyleSheet('border:None')
        self.btn.clicked.connect(self.exit)
        
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(285,349,228,293)
        self.label_7.setObjectName('label_7')
        
        self.th = Thread(self)
        self.th.changePixmap.connect(self.label.setPixmap)
        self.th.start()
        
        self.th2 = Thread2(self)
        self.th2.changePixmap.connect(self.label_5.setPixmap)
        self.th2.start()
        
        self.th3 = Thread3(self)
        self.th3.changePixmap.connect(self.label_6.setPixmap)
        self.th3.start()
        
        self.th4 = Thread4(self)
        self.th4.changePixmap.connect(self.label_7.setPixmap)
        self.th4.start()
        
        MainWindow.setCentralWidget(self.centralwidget)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        # self.lineEdit_2.returnPressed.connect(self.open)
        # print("test")

    def exit(self):
        sys.exit()
    
    def open(self):
        image_files = self.get_files('D:\\Development\\bugyungde\\imagmovie_test\\')

        img = cv2.imread(image_files[0])
        height,width,channel = img.shape
        fps = 30

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        writer = cv2.VideoWriter(BASE_DIR + '/' + 'output3.mp4', fourcc, fps, (width, height))

        for file in image_files:

            img = cv2.imread(file)

            writer.write(img)

            cv2.imshow("Color", img)

            # ESC키 누르면 중지
            if cv2.waitKey(33) == 27:
                break

    def get_files(self, path):
        for root, subdirs, files in os.walk(path):
    
            list_files = []

            if len(files) > 0:
                for f in files:
                    fullpath = root + '/' + f
                    list_files.append(fullpath)

            return list_files

    # def open(self):
    #     global gcount
    #     self.label.setText("이대로 진행 하시겠습니까?")     
    #     if gcount < 5:
    #         self.lineEdit_2.returnPressed.connect(self.rejult)
    #         self.label_6.setText(str(gcount))
    #         gcount += 1
    #     else :
    #         self.delay()

    # def delay(self):
    #     for i in range(5):
    #         time.sleep(1)
    #         self.label_6.setText(str(i))            

    def rejult(self):         
        text = self.lineEdit.text()
        text2 = self.lineEdit_2.text()
        config = configparser.ConfigParser()
        config.read("ai.ini")
        pid = config['user']['id']
        ppw = config['user']['pw']
        if text == pid and text2 == ppw:
            #self.label.setText("open")
            self.label_3.setPixmap(QtGui.QPixmap("test.png"))
            self.label.setHidden(True)
            self.label_2.setHidden(True)
            self.lineEdit.setHidden(True)
            self.lineEdit_2.setHidden(True)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        # MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        #self.label.setText(_translate("MainWindow", "ID"))
        #self.label_2.setText(_translate("MainWindow", "PW"))

class Thread(QThread):
    changePixmap = pyqtSignal(QtGui.QPixmap)
    def __init__(self, parent=None):
        QThread.__init__(self, parent=parent)
        self.isRunning = True
    def run(self):
            cap = cv2.VideoCapture("an.mp4")
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
                p = convertToQtFormat.scaled(227, 300, Qt.IgnoreAspectRatio)
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
        
class Thread2(QThread):
    changePixmap = pyqtSignal(QtGui.QPixmap)
    def __init__(self, parent=None):
        QThread.__init__(self, parent=parent)
        self.isRunning = True
    def run(self):
            cap = cv2.VideoCapture("kim.mp4")
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
                p = convertToQtFormat.scaled(227, 300, Qt.IgnoreAspectRatio)
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
            cap = cv2.VideoCapture("karina.mp4")
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
                p = convertToQtFormat.scaled(227, 300, Qt.IgnoreAspectRatio)
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
        self.isRunning = True
    def run(self):
            cap = cv2.VideoCapture("sana.mp4")
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
                p = convertToQtFormat.scaled(284, 347, Qt.IgnoreAspectRatio)
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
        

if __name__ == "__main__":
    import sys #object는 윈도의 최고 조상
    app = QtWidgets.QApplication(sys.argv) # sys.argv는 현재 작업중인.py 절대 경로를 인자로 넘겨줌
    MainWindow = QtWidgets.QMainWindow() #윈도우 UI를 연결하기 위한 상속
    ui = Ui_MainWindow() #위 클래스를 ui 변수에 넣는다 여기서 부터 클래스 개념 필요
    ui.setupUi(MainWindow) #위 QtWidgets.QMainWindows()에서 상속받아서 위 SetupUi함수 인자로 넘겨줌 즉 위젯 실행하라는 뜻
    MainWindow.show() #MainWindow를 화면에 표시
    sys.exit(app.exec_()) #무한루프


