a='rtsp://210.99.70.120:1935/live/cctv001.stream'
b=a.split('/')
c=b[-1].split('.')
print(c[0])