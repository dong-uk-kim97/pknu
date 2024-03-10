import sqlite3
t1='cctv001'
t2=t1.upper()
con = sqlite3.connect('C:\\study\\20240213\\python_db\\friend.db')
cur = con.cursor()
cur.execute(f'SELECT 경도, 위도, RTSP FROM CCND WHERE CCTV="{t2}"')
a=cur.fetchone()
print(a)
# longitude = a[0]
# latitude = a[1]
# path = a[2]
# cur.execute('INSERT OR IGNORE INTO CCND (save_path) VALUES (?,)',(save_path))
con.commit()
con.close()