import cv2
import os

# 동영상 파일의 경로
video_path = "./an.mp4"

# 동영상 파일 열기
video = cv2.VideoCapture(video_path)

# 동영상의 프레임 수
frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

# 프레임을 이미지로 변환하고 파일로 저장
for i in range(frame_count):
    ret, frame = video.read()
    os.makedirs('./image',exist_ok=True)
    if ret:
        image_path = f"./image/an_{i}.jpg"
        cv2.imwrite(image_path, frame)

# 동영상 파일 닫기
video.release()