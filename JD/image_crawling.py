import cv2

# 동영상 파일의 경로
video_path = "rtsp://210.99.70.120:1935/live/cctv023.stream"

# 동영상 파일 열기
video = cv2.VideoCapture(video_path)
count = 0
# 프레임을 이미지로 변환하고 파일로 저장
while True:
    ret, frame = video.read()
    if ret:
        image_path = f"C:\\study\\JD\\images\\10\\{count}.jpg"
        cv2.imwrite(image_path, frame)
        count +=1