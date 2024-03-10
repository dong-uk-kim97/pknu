import folium
import webbrowser
import base64
import pandas as pd
import os
import time
from folium.plugins import MiniMap
import warnings
warnings.filterwarnings(action='ignore')

a = pd.read_csv('C:\\study\\20240213\\python_db\\cctv.csv', encoding="cp949")
b= pd.read_excel('C:\\study\\20240216\\a.xlsx')
m = folium.Map(location=[35.1347223, 129.107886], # 위도, 경도
               zoom_start=12,
               tiles='Esri.WorldImagery')

minimap = MiniMap()
minimap.add_to(m)

latlon=[
    [35.248905, 129.095482],
    
 ]

latlon1=[
    [35.105336, 129.030977]
]

pic = base64.b64encode(open('pukyong.png', 'rb').read()).decode()
image_tag = '<img src="data:image/jpeg;base64,{}">'.format(pic)
iframe = folium.IFrame(image_tag, width=700, height=120)
popup = folium.Popup(iframe, max_width=650)

for i in range(a.shape[0]):
    folium.Marker([a.iloc[i]['위도'], a.iloc[i]['경도']], # 위도, 경도
                  popup = f'<strong>{a.iloc[i]["설치위치명"]}</strong>', #마우스 클릭시 표기되는 문구
                  tooltip="click").add_to(m)
    
for i in range(len(latlon)):
    folium.Marker(latlon[i],
                  icon= folium.Icon(color='red', icon='star'),
                  popup=popup,
                  tooltip="부경대학교").add_to(m)
    
for i in range(len(latlon1)):
    folium.Marker(latlon1[i],
                  icon= folium.Icon(color='red', icon='star'),
                  popup="popup",
                  tooltip="우리집").add_to(m)

for i in range(16):
    pic = base64.b64encode(open(f'C:\\study\\20240216\\test{i}.jpg', 'rb').read()).decode()
    image_tag = '<img src="data:image/jpeg;base64,{}">'.format(pic)
    iframe = folium.IFrame(image_tag, width=1200, height=1020)
    popup = folium.Popup(iframe, max_width=1200)
    folium.Marker([b.iloc[i]['위도'],b.iloc[i]['경도']],
                  popup=popup,
                  icon= folium.Icon(color='black', icon='star'),
                  tooltip='click here').add_to(m)


m.save('filename.html')
webbrowser.open_new_tab('filename.html')
time.sleep(5)
os.system('taskkill /im chrome.exe /f')
time.sleep(0.1)