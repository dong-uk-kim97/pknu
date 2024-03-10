import sqlite3
import pandas as pd

df = pd.read_excel('TAAS.xlsx')
con = sqlite3.connect('taas.db')
cur = con.cursor()
df.to_sql('taas', con=con, if_exists='replace', index=False)
con.close()