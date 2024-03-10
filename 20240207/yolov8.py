from ultralytics import YOLO

# Load a pre-trained YOLOv8 model
model = YOLO('yolov8s.pt')

# Specify the source image
source = "rtsp://210.99.70.120:1935/live/cctv006.stream"

# Make predictions
results = model.predict(source, save=True, imgsz=640, show=True, conf=0.2,
                        line_width=1,save_conf=True)

# Extract bounding box dimensions
boxes = results[0].boxes.xywh.gpu()
for box in boxes:
    x, y, w, h = box
    print(f"Width of Box: {w}, Height of Box: {h}")