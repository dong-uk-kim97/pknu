import sqlite3
import pandas as pd
from sqlite3 import Error

conn = sqlite3.connect('friend.db') # db를 생성 해당 폴더에 DB가 있으면 불러 오고 없으면 생성

cur = conn.cursor() # 커서 객체 생성
# cur.execute("DROP table cctv.csv;")
cur.execute("DROP table CCND")
df = pd.read_csv('cctv.csv', encoding='cp949')
df.to_sql('CCND', con=conn, if_exists='replace', index=False)
# conn.commit()
conn.close()