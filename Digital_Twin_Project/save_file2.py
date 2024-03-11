import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import QThread
import os
from datetime import datetime
import sqlite3
import cv2
import time

save_path=""
save_path1=""
save_path2=""
save_path3=""
save_path4=""
save_path5=""
save_path6=""
save_path7=""
save_path8=""
save_path9=""

class Sticker(QtWidgets.QMainWindow):
    def __init__(self):
        super(Sticker, self).__init__()
        self.setupUi()

    def setupUi(self):
        centralWidget = QtWidgets.QWidget(self)
        self.setCentralWidget(centralWidget)

        flags = QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowFlags(flags)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground, True)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.save_db()
        print('save')
        self.save_thread()

    def save_db(self):
        global save_path, save_path1,save_path2,save_path3,save_path4,save_path5,save_path6,save_path7,save_path8,save_path9
        now = datetime.now()
        now1 = now.strftime('%Y\\%m\\%d\\%H')
        save_path = f'C:\\{now1}'
        con = sqlite3.connect('rtsp.db',check_same_thread=False)
        cur = con.cursor()
        cur.execute('SELECT lat, long FROM rtsp WHERE save_path IS NULL ORDER BY ID DESC LIMIT 9')
        a=cur.fetchall()
        
        longitude1 = a[8][1]
        latitude1 = a[8][0]
        longitude2 = a[7][1]
        latitude2 = a[7][0]
        longitude3 = a[6][1]
        latitude3 = a[6][0]
        longitude4 = a[5][1]
        latitude4 = a[5][0]
        longitude5 = a[4][1]
        latitude5 = a[4][0]
        longitude6 = a[3][1]
        latitude6 = a[3][0]
        longitude7 = a[2][1]
        latitude7 = a[2][0]
        longitude8 = a[1][1]
        latitude8 = a[1][0]
        longitude9 = a[0][1]
        latitude9 = a[0][0]
        
        save_path1 = f'{save_path}\\seoul_dongdaemungu_{longitude1}_{latitude1}SEOULCCTV_A_1.avi'
        save_path2 = f'{save_path}\\seoul_dongdaemungu_{longitude2}_{latitude2}SEOULCCTV_A_2.avi'
        save_path3 = f'{save_path}\\seoul_seodaemungu_{longitude3}_{latitude3}SEOULCCTV_B_1.avi'
        save_path4 = f'{save_path}\\seoul_jonro1_{longitude4}_{latitude4}SEOULCCTV_C_1.avi'
        save_path5 = f'{save_path}\\seoul_jonro1_{longitude5}_{latitude5}SEOULCCTV_C_2.avi'
        save_path6 = f'{save_path}\\seoul_jungu_{longitude6}_{latitude6}SEOULCCTV_D_1.avi'
        save_path7 = f'{save_path}\\seoul_jonro2_{longitude7}_{latitude7}SEOULCCTV_E_1.avi'
        save_path8 = f'{save_path}\\seoul_jonro2_{longitude8}_{latitude8}SEOULCCTV_E_2.avi'
        save_path9 = f'{save_path}\\seoul_jonro2_{longitude9}_{latitude9}SEOULCCTV_E_3.avi'
        print(save_path9)
        
        cur.execute(f'UPDATE rtsp SET save_path="{save_path1}" WHERE rtsp_path ="rtsp://210.99.70.120:1935/live/cctv010.stream"')
        cur.execute(f'UPDATE rtsp SET save_path="{save_path2}" WHERE rtsp_path ="rtsp://210.99.70.120:1935/live/cctv011.stream"')
        cur.execute(f'UPDATE rtsp SET save_path="{save_path3}" WHERE rtsp_path ="rtsp://210.99.70.120:1935/live/cctv012.stream"')
        cur.execute(f'UPDATE rtsp SET save_path="{save_path4}" WHERE rtsp_path ="rtsp://210.99.70.120:1935/live/cctv019.stream"')
        cur.execute(f'UPDATE rtsp SET save_path="{save_path5}" WHERE rtsp_path ="rtsp://210.99.70.120:1935/live/cctv020.stream"')
        cur.execute(f'UPDATE rtsp SET save_path="{save_path6}" WHERE rtsp_path ="rtsp://210.99.70.120:1935/live/cctv015.stream"')
        cur.execute(f'UPDATE rtsp SET save_path="{save_path7}" WHERE rtsp_path ="rtsp://210.99.70.120:1935/live/cctv024.stream"')
        cur.execute(f'UPDATE rtsp SET save_path="{save_path8}" WHERE rtsp_path ="rtsp://210.99.70.120:1935/live/cctv026.stream"')
        cur.execute(f'UPDATE rtsp SET save_path="{save_path9}" WHERE rtsp_path ="rtsp://210.99.70.120:1935/live/cctv018.stream"')            
        con.commit()
        con.close()
        os.makedirs(f'{save_path}',exist_ok=True)
        
    def save_thread(self):    
        self.th1 = Thread1(self)
        self.th1.start()
        self.th2 = Thread2(self)
        self.th2.start()
        self.th3 = Thread3(self)
        self.th3.start()
        self.th4 = Thread4(self)
        self.th4.start()
        self.th5 = Thread5(self)
        self.th5.start()
        self.th6 = Thread6(self)
        self.th6.start()
        self.th7 = Thread7(self)
        self.th7.start()
        self.th8 = Thread8(self)
        self.th8.start()
        self.th9 = Thread9(self)
        self.th9.start()

class Thread1(QThread):
    def __init__(self,parent=None):
        QThread.__init__(self, parent=parent)
        self.isRunning = True

    def run(self):
        global save_path1
        try:
            cap = cv2.VideoCapture('rtsp://210.99.70.120:1935/live/cctv010.stream')
            if not cap.isOpened():
                cap.release()
            
            fourcc=cv2.VideoWriter_fourcc(*'DIVX')
            w = round(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            h = round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            out = cv2.VideoWriter(f'{save_path1}', fourcc, 15, (w, h))

            while True:
                ret, frame = cap.read()
                if ret:
                    out.write(frame)
                else:
                    cap.release()
                    print('ret=', ret)
                    break
        
        except Exception as e:
            print(e)
   
class Thread2(QThread):
    def __init__(self,parent=None):
        QThread.__init__(self, parent=parent)
        self.isRunning = True

    def run(self):
        global save_path2
        try:
            cap = cv2.VideoCapture('rtsp://210.99.70.120:1935/live/cctv011.stream')
            if not cap.isOpened():
                cap.release()
            
            fourcc=cv2.VideoWriter_fourcc(*'DIVX')
            w = round(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            h = round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            out = cv2.VideoWriter(f'{save_path2}', fourcc, 15, (w, h))

            while True:
                ret, frame = cap.read()
                if ret:
                    out.write(frame)
                else:
                    cap.release()
                    print('ret=', ret)
                    break
        
        except Exception as e:
            print(e)

class Thread3(QThread):
    def __init__(self,parent=None):
        QThread.__init__(self, parent=parent)
        self.isRunning = True

    def run(self):
        global save_path3
        try:          
            os.makedirs(f'{save_path3}',exist_ok=True)
            cap = cv2.VideoCapture("rtsp://210.99.70.120:1935/live/cctv012.stream")
            if not cap.isOpened():
                cap.release()
            
            fourcc=cv2.VideoWriter_fourcc(*'DIVX')
            w = round(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            h = round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            out = cv2.VideoWriter(f'{save_path3}', fourcc, 15, (w, h))

            while True:
                ret, frame = cap.read()
                if ret:
                    out.write(frame)
                else:
                    cap.release()
                    print('ret=', ret)
                    break
            
        except Exception as e:
            print(e)

class Thread4(QThread):
    def __init__(self,parent=None):
        QThread.__init__(self, parent=parent)
        self.isRunning = True

    def run(self):
        global save_path4
        try:
            cap = cv2.VideoCapture("rtsp://210.99.70.120:1935/live/cctv019.stream")
            if not cap.isOpened():
                cap.release()
            
            fourcc=cv2.VideoWriter_fourcc(*'DIVX')
            w = round(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            h = round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            out = cv2.VideoWriter(f'{save_path4}', fourcc, 15, (w, h))

            while True:
                ret, frame = cap.read()
                if ret:
                    out.write(frame)
                else:
                    cap.release()
                    print('ret=', ret)
                    break
            
        except Exception as e:
            print(e)

class Thread5(QThread):
    def __init__(self,parent=None):
        QThread.__init__(self, parent=parent)
        self.isRunning = True

    def run(self):
        global save_path5
        try:
            cap = cv2.VideoCapture("rtsp://210.99.70.120:1935/live/cctv020.stream")
            if not cap.isOpened():
                cap.release()
            
            fourcc=cv2.VideoWriter_fourcc(*'DIVX')
            w = round(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            h = round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            out = cv2.VideoWriter(f'{save_path5}', fourcc, 15, (w, h))

            while True:
                ret, frame = cap.read()
                if ret:
                    out.write(frame)
                else:
                    cap.release()
                    print('ret=', ret)
                    break
            
        except Exception as e:
            print(e)

class Thread6(QThread):
    def __init__(self,parent=None):
        QThread.__init__(self, parent=parent)
        self.isRunning = True

    def run(self):
        global save_path6
        try:
            cap = cv2.VideoCapture("rtsp://210.99.70.120:1935/live/cctv015.stream")
            if not cap.isOpened():
                cap.release()
            
            fourcc=cv2.VideoWriter_fourcc(*'DIVX')
            w = round(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            h = round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            out = cv2.VideoWriter(f'{save_path6}', fourcc, 15, (w, h))

            while True:
                ret, frame = cap.read()
                if ret:
                    out.write(frame)
                else:
                    cap.release()
                    print('ret=', ret)
                    break
            
        except Exception as e:
            print(e)

class Thread7(QThread):
    def __init__(self,parent=None):
        QThread.__init__(self, parent=parent)
        self.isRunning = True

    def run(self):
        global save_path7
        try:
            cap = cv2.VideoCapture('rtsp://210.99.70.120:1935/live/cctv024.stream')
            if not cap.isOpened():
                cap.release()
            
            fourcc=cv2.VideoWriter_fourcc(*'DIVX')
            w = round(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            h = round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            out = cv2.VideoWriter(f'{save_path7}', fourcc, 15, (w, h))

            while True:
                ret, frame = cap.read()
                if ret:
                    out.write(frame)
                else:
                    cap.release()
                    print('ret=', ret)
                    break
            
        except Exception as e:
            print(e)

class Thread8(QThread):
    def __init__(self,parent=None):
        QThread.__init__(self, parent=parent)
        self.isRunning = True

    def run(self):
        global save_path8
        try:
            cap = cv2.VideoCapture("rtsp://210.99.70.120:1935/live/cctv026.stream")
            if not cap.isOpened():
                cap.release()
            
            fourcc=cv2.VideoWriter_fourcc(*'DIVX')
            w = round(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            h = round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            out = cv2.VideoWriter(f'{save_path8}', fourcc, 15, (w, h))

            while True:
                ret, frame = cap.read()
                if ret:
                    out.write(frame)
                else:
                    cap.release()
                    print('ret=', ret)
                    break
            
        except Exception as e:
            print(e)
       

class Thread9(QThread):
    def __init__(self,parent=None):
        QThread.__init__(self, parent=parent)
        self.isRunning = True

    def run(self):
        global save_path9
        try:
            cap = cv2.VideoCapture("rtsp://210.99.70.120:1935/live/cctv018.stream")
            if not cap.isOpened():
                cap.release()
            
            fourcc=cv2.VideoWriter_fourcc(*'DIVX')
            w = round(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            h = round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            out = cv2.VideoWriter(f'{save_path9}', fourcc, 15, (w, h))

            while True:
                ret, frame = cap.read()
                if ret:
                    out.write(frame)
                else:
                    cap.release()
                    print('ret=', ret)
                    break
            
        except Exception as e:
            print(e)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    sticker=Sticker()
    sticker.show()
    sys.exit(app.exec_())