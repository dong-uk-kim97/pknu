import os
import time
import pandas as pd

df = pd.read_excel('C:\\study\\20240216\\a.xlsx')
df_1 = df['이미지URL'].values.tolist()
print(df_1)


# 다운받을 이미지 url
url = df_1
# time check
start = time.time()

count = 0
# curl 요청
for i in url:
    os.system("curl " + i + f" > test{count}.jpg")
    count += 1

# 이미지 다운로드 시간 체크
print(time.time() - start)