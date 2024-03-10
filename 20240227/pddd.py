import pandas as pd
import numpy as np
import sqlite3

df = pd.read_html('https://en.wikipedia.org/wiki/All-time_Olympic_Games_medal_table', header = 0, index_col = 0)
#print(df)
summer = df[1].iloc[1:, :5]
#print(summer)
summer.columns = ['경기수', '금', '은', '동', '계']
#print(summer.sort_values('금', ascending = False))

summer.to_excel('하계동계올림픽.xlsx')
con = sqlite3.connect("orimpiccc.db")
summer.to_sql("table_name", con, if_exists="append", index=False)

con.close()
