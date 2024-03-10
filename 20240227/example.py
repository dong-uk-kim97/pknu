import folium
import folium as g
import webbrowser
import base64
import pandas as pd
import sqlite3
from folium.plugins import MarkerCluster
import requests
import json

r = requests.get('https://raw.githubusercontent.com/southkorea/seoul-maps/master/kostat/2013/json/seoul_municipalities_geo_simple.json')
c = r.content
seoul_geo = json.loads(c)

#기준이 되는 map 설정 및 크기 설정
m = folium.Map(location=[37.5518911, 126.9917937],
               zoom_start=12)
folium.GeoJson(
    seoul_geo,
    name='지역구'
).add_to(m)

# SQLite3 데이터베이스 연결
conn = sqlite3.connect("taas.db")
cur = conn.cursor()

# 데이터베이스에서 데이터 가져오기
cur.execute('SELECT LOCATION_Y, LOCATION_X, ADDRESS_JIBUN FROM taas WHERE ADDRESS_JIBUN LIKE "서울%"') 
data = cur.fetchall()

# 데이터베이스 연결 종료
conn.close()

# df = pd.read_excel('hospital.xlsx')



marker_cluster = MarkerCluster().add_to(m)

# 데이터에서 위치 정보 추출하고 지도에 마커 추가하기
for item in data:
    lat = item[0]
    lon = item[1]
    popup = item[2]
    folium.Marker([lat, lon]).add_to(marker_cluster)

# for i in range(df.shape[0]):
#     lat = df.iloc[i]['경도']
#     lon = df.iloc[i]['위도']
#     popup = df.iloc[i]['이름']
#     folium.Marker([lat,lon], icon= folium.Icon(color='red', icon='star')).add_to(m)


m.save('filename2.html')
webbrowser.open_new_tab('filename2.html')