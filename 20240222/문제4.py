import sqlite3
import os

# 폴더가 없으면
os.makedirs('C:\\data',exist_ok=True)
con = sqlite3.connect('C:\\data\\First.db')
