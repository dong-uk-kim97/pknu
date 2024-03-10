"""
import folium
from folium.plugins import HeatMap

m = folium.Map(location=[35.89747, 127.092337], zoom_start=13)

m.save("index.html")
"""
import folium
import webbrowser
import base64
import warnings
warnings.filterwarnings(action='ignore')


m = folium.Map(location=[35.1347223, 129.107886], # 위도, 경도
               zoom_start=12)

latlon=[
    [35.1347223, 129.107886],
]

# pic = base64.b64encode(open('sum.jpg', 'rb').read()).decode()
# image_tag = '<img src="data:image/jpeg;base64,{}">'.format(pic)
# iframe = folium.IFrame(image_tag, width=230, height=100)
# popup = folium.Popup(iframe, max_width=650)

for i in range(len(latlon)):
    folium.Marker(latlon[i],
                  popup = 'popup',
                  tooltip="부경대학교").add_to(m) 


m.save('filename.html')
webbrowser.open_new_tab('filename.html')