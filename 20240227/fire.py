import sqlite3
import pandas as pd

con = sqlite3.connect('fire.db')
cur = con.cursor()
df = pd.read_csv('fire.csv', encoding='cp949')
df=df[df['시도']=='서울특별시']
df=df[(df['화재발생(월)']==1)|(df['화재발생(월)']==7)|(df['화재발생(월)']==8)|(df['화재발생(월)']==12)]
df.to_sql('fire', con=con, if_exists='replace', index=False)
con.close()