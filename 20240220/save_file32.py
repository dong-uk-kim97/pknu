# save_file.py
import os
from datetime import datetime
import sqlite3
import cv2
# import pandas as pd

def save_thread():
    try:
        print('Function Start!')
        now = datetime.now()
        now1 = now.strftime('%Y\\%m\\%d\\%H')
        save_path = f'C:\\{now1}'
        con = sqlite3.connect('C:\\study\\20240219\\rtsp.db')
        cur = con.cursor()
        cur.execute('SELECT path FROM Rtsp WHERE save_path IS NULL ORDER BY ID DESC LIMIT 4')
        a=cur.fetchall()
        con.commit()
        con.close()
        c= a[3][0]
        print(c)
        
        
        con = sqlite3.connect('C:\\study\\20240219\\rtsp.db')
        cur = con.cursor()
        cur.execute(f'SELECT 경도, 위도, RTSP FROM cctv WHERE RTSP="{c}"')
        b=cur.fetchone()
        longitude = b[0]
        latitude = b[1]
        con.commit()
        con.close()
        save_path1 = f'{save_path}\\busan_south_{longitude}_{latitude}CCNDCCTV_A.avi'
        
        con = sqlite3.connect('C:\\study\\20240219\\rtsp.db')
        cur = con.cursor()
        cur.execute(f'UPDATE Rtsp SET save_path="{save_path1}" WHERE path = "{c}"')
        con.commit()
        con.close()
        
        os.makedirs(f'{save_path}',exist_ok=True)
        cap = cv2.VideoCapture(c)
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
        # print('Function END!')
        
    except Exception as e:
        print(e)
            
def save_thread2():
    try:
        print('Function Start!')
        now = datetime.now()
        now1 = now.strftime('%Y\\%m\\%d\\%H')
        save_path = f'C:\\{now1}'
        con = sqlite3.connect('C:\\study\\20240219\\rtsp.db')
        cur = con.cursor()
        cur.execute('SELECT path FROM Rtsp WHERE save_path IS NULL ORDER BY ID DESC LIMIT 4')
        a=cur.fetchall()
        con.commit()
        con.close()
        c= a[2][0]
        print(c)
        
        
        con = sqlite3.connect('C:\\study\\20240219\\rtsp.db')
        cur = con.cursor()
        cur.execute(f'SELECT 경도, 위도, RTSP FROM cctv WHERE RTSP="{c}"')
        b=cur.fetchone()
        longitude = b[0]
        latitude = b[1]
        con.commit()
        con.close()
        save_path1 = f'{save_path}\\busan_south_{longitude}_{latitude}CCNDCCTV_B.avi'
        
        con = sqlite3.connect('C:\\study\\20240219\\rtsp.db')
        cur = con.cursor()
        cur.execute(f'UPDATE Rtsp SET save_path="{save_path1}" WHERE path = "{c}"')
        con.commit()
        con.close()
        
        os.makedirs(f'{save_path}',exist_ok=True)
        cap = cv2.VideoCapture(c)
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
        # print('Function END!')
        
    except Exception as e:
        print(e)
def save_thread3():
    try:
        print('Function Start!')
        now = datetime.now()
        now1 = now.strftime('%Y\\%m\\%d\\%H')
        save_path = f'C:\\{now1}'
        con = sqlite3.connect('C:\\study\\20240219\\rtsp.db')
        cur = con.cursor()
        cur.execute('SELECT path FROM Rtsp WHERE save_path IS NULL ORDER BY ID DESC LIMIT 4')
        a=cur.fetchall()
        con.commit()
        con.close()
        c= a[1][0]
        print(c)
        
        
        con = sqlite3.connect('C:\\study\\20240219\\rtsp.db')
        cur = con.cursor()
        cur.execute(f'SELECT 경도, 위도, RTSP FROM cctv WHERE RTSP="{c}"')
        b=cur.fetchone()
        longitude = b[0]
        latitude = b[1]
        con.commit()
        con.close()
        save_path1 = f'{save_path}\\busan_south_{longitude}_{latitude}CCNDCCTV_C.avi'
        
        con = sqlite3.connect('C:\\study\\20240219\\rtsp.db')
        cur = con.cursor()
        cur.execute(f'UPDATE Rtsp SET save_path="{save_path1}" WHERE path = "{c}"')
        con.commit()
        con.close()
        
        os.makedirs(f'{save_path}',exist_ok=True)
        cap = cv2.VideoCapture(c)
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
        # print('Function END!')
        
    except Exception as e:
        print(e)
            
def save_thread4():
    try:
        print('Function Start!')
        now = datetime.now()
        now1 = now.strftime('%Y\\%m\\%d\\%H')
        save_path = f'C:\\{now1}'
        con = sqlite3.connect('C:\\study\\20240219\\rtsp.db')
        cur = con.cursor()
        cur.execute('SELECT path FROM Rtsp WHERE save_path IS NULL ORDER BY ID DESC LIMIT 4')
        a=cur.fetchall()
        con.commit()
        con.close()
        c= a[0][0]
        print(c)
        
        
        con = sqlite3.connect('C:\\study\\20240219\\rtsp.db')
        cur = con.cursor()
        cur.execute(f'SELECT 경도, 위도, RTSP FROM cctv WHERE RTSP="{c}"')
        b=cur.fetchone()
        longitude = b[0]
        latitude = b[1]
        con.commit()
        con.close()
        save_path1 = f'{save_path}\\busan_south_{longitude}_{latitude}CCNDCCTV_D.avi'
        
        con = sqlite3.connect('C:\\study\\20240219\\rtsp.db')
        cur = con.cursor()
        cur.execute(f'UPDATE Rtsp SET save_path="{save_path1}" WHERE path = "{c}"')
        con.commit()
        con.close()
        
        os.makedirs(f'{save_path}',exist_ok=True)
        cap = cv2.VideoCapture(c)
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
        # print('Function END!')
        
    except Exception as e:
        print(e)
        
if __name__ == "__main__":
    save_thread()
    save_thread2()
    save_thread3()
    save_thread4()