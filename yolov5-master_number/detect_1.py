# YOLOv5 🚀 by Ultralytics, AGPL-3.0 license
"""
Run YOLOv5 detection inference on images, videos, directories, globs, YouTube, webcam, streams, etc.

Usage - sources: # weights는 직접 학습된 모델 또는 yolo가 기본으로 제공해주는 모델의 종류, source는 어떤 조류의 인식을 사용할 것인지 정함
    $ python detect.py --weights yolov5s.pt --source 0                               # webcam
                                                     img.jpg                         # image
                                                     vid.mp4                         # video
                                                     screen                          # screenshot
                                                     path/                           # directory
                                                     list.txt                        # list of images
                                                     list.streams                    # list of streams
                                                     'path/*.jpg'                    # glob
                                                     'https://youtu.be/LNwODJXcvt4'  # YouTube
                                                     'rtsp://example.com/media.mp4'  # RTSP, RTMP, HTTP stream //카메라 영상을 접속해서 인식하기 위한 구문
source별 이미지, 동영상, RTSP 등을 선택해서 사용

모델을 선정 모델에 맞게 속도를 빠르게 하고 싶으면 인식률은 조금 낮아도 yolov5s 속도는 느려도 인식률을 높이고 싶으면 yolov5x
Usage - formats:
    $ python detect.py --weights yolov5s.pt                 # PyTorch
                                 yolov5s.torchscript        # TorchScript
                                 yolov5s.onnx               # ONNX Runtime or OpenCV DNN with --dnn
                                 yolov5s_openvino_model     # OpenVINO
                                 yolov5s.engine             # TensorRT
                                 yolov5s.mlmodel            # CoreML (macOS-only)
                                 yolov5s_saved_model        # TensorFlow SavedModel
                                 yolov5s.pb                 # TensorFlow GraphDef
                                 yolov5s.tflite             # TensorFlow Lite
                                 yolov5s_edgetpu.tflite     # TensorFlow Edge TPU
                                 yolov5s_paddle_model       # PaddlePaddle
기존 머신러닝 및 딥러닝은 Tensorflow, keras를 사용하였으나 Yolov5부터는 PyTorch를 사용하여 성능을 최대화로 올림 
"""

import argparse # cmd 동작을 시키기 위한 클래스(epoch, batch_size, ir_initial)
import csv
import os
import platform
import sys
from pathlib import Path

import torch # PyTorch 불러옴
# facebook에서 제공하는 딥러닝 도구로서, numpy와 효율적인 연동을 지원하는 편리한 도구이다.
# 구글에서는 tensorflow에서 개발
# tensorflow나 pytorch나 기본적인 data structure은 tensor이다.
# tensor란 2차원 이상의 array이며, matrix, vector의 일반화된 객체이다.

# 일반화된 정의 : 
# vector는 1차원 tensor이다.
# matrix는 2차원 tensor이다.
# 색을 나타내는 RGB는 3차원 tensor이다.

# 학습 및 인식에는 두 가지 방법이 있는데 CPU사용과 GPU(CUDA)사용으로 앞의 소스코드는 GPU가 있다면 불러와서 사용하겠다고 선언
import torch.backends.cudnn as cudnn
global_list_num = None

FILE = Path(__file__).resolve() # 현재 .py의 경로를 불러와서 FILE에 대입
ROOT = FILE.parents[0]  # YOLOv5 root directory 
if str(ROOT) not in sys.path: # 만약 ROOT가 없다면 
    sys.path.append(str(ROOT))  # add ROOT to PATH 한번 더 시도 sys.path에 현재 폴더를 추가하여 import가 가능해짐
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative ROOT를 찾았다면 경로와 cwd를 ROOT에 대입 relative ROOT와 터미널 현재 위치와의 상대경로 

expe = 0
expe_f = 0
check_image =""
sellect = 0

# YOLO를 사용하기 위한 선언으로 YOLO 관련 사용을 선언한 구문 
from ultralytics.utils.plotting import Annotator, colors, save_one_box

from models.common import DetectMultiBackend
from utils.dataloaders import IMG_FORMATS, VID_FORMATS, LoadImages, LoadScreenshots, LoadStreams
from utils.general import (
    LOGGER,
    Profile,
    check_file,
    check_img_size,
    check_imshow,
    check_requirements,
    colorstr,
    cv2,
    increment_path,
    non_max_suppression,
    print_args,
    scale_boxes,
    strip_optimizer,
    xyxy2xywh,
)
from utils.torch_utils import select_device, smart_inference_mode
# from PIL import Image # opencv로 이미지 또는 영상을 imshow()할 수 있고, 아니면 PIL로 이미지 또는 영상을 show할 수 있다.

@smart_inference_mode()
def run(
    weights=ROOT / "best.pt",  # model path or triton URL
    source=ROOT / "../car_plate/image3/val/images",  # file/dir/URL/glob/screen/0(webcam) 인식 시킬 폴더 경로
    data=ROOT / "data/coco128.yaml",  # dataset.yaml path 클래스가 정의 되어 있는 파일 
    # imgsz=(640, 640),  # inference size (height, width)
    imgsz=(416, 416),  # inference size (height, width)
    conf_thres=0.25,  # confidence threshold
    iou_thres=0.45,  # NMS IOU threshold
    max_det=1000,  # maximum detections per image
    device="",  # cuda device, i.e. 0 or 0,1,2,3 or cpu
    view_img=False,  # show results
    save_txt=False,  # save results to *.txt
    save_csv=False,  # save results in CSV format
    save_conf=False,  # save confidences in --save-txt labels
    save_crop=False,  # save cropped prediction boxes
    nosave=False,  # do not save images/videos
    classes=None,  # filter by class: --class 0, or --class 0 2 3
    agnostic_nms=False,  # class-agnostic NMS
    augment=False,  # augmented inference
    visualize=False,  # visualize features
    update=False,  # update all models
    project=ROOT / "",  # save results to project/name
    name="",  # save results to project/name
    exist_ok=False,  # existing project/name ok, do not increment exist는 원하는 폴더에 파일이 있는지 없는지 알기 위한 구문 
    line_thickness=1,  # bounding box thickness (pixels) 박스 굵기
    hide_labels=False,  # hide labels
    hide_conf=False,  # hide confidences
    half=False,  # use FP16 half-precision inference
    dnn=False,  # use OpenCV DNN for ONNX inference
    vid_stride=1,  # video frame-rate stride
):
    global expe, check_image, sellect, expe_f
    source = str(source) # 인식을 시킬 이미지들이 담겨 있는 경로
    check_image = None # check_image에 None값을 대입 즉 초기화
    save_img = not nosave and not source.endswith(".txt")  # save inference images 확장자를 구분하기 위한 구문 save inference images not의 의미 뒤에 오는 조건문이 거짓이면 조건을 만족
    is_file = Path(source).suffix[1:] in (IMG_FORMATS + VID_FORMATS) # IMG_FORMATS + VID_FORMATS값을 is_file의 처음부터 파일이 있는 끝까지 읽어와서 is_file에 대입 
    # .suffix는 경로에 지정된 파일의 파일 확장자(점 포함)를 반환하는 메서드
    # [1:] 두번째 위치 이후의 모든 문자(즉 점제외)를 추출하는 슬라이스 작업
    # 파일 확장자가 이미지형식(.jpg, .png)등에 해당하는 경우 표현식은 True
    # 파일 확장자가 비디오형식(.mp4, .avi)등에 해당하는 경우 표현식은 True
    # 즉 확장자에 따라서 이미지인지 비디오인지를 판별하기 위한 구문 
    is_url = source.lower().startswith(("rtsp://", "rtmp://", "http://", "https://")) # 통신 경로를 선택 
    # .lower()은 모든 문자를 소문자로 변환하는 메서드
    # .startswith()은 문자열이 지정된 접두사로 시작하는지 확인 
     
    webcam = source.isnumeric() or source.endswith(".streams") or (is_url and not is_file) # 웹캠을 사용하기 위한 구문
    # .isnumeric()은 문자열의 모든 문자가 숫자이면 True, 그렇지 않으면 False를 반환하는 메서드
    
    screenshot = source.lower().startswith("screen")
    if is_url and is_file:
        source = check_file(source)  # download

    # Directories
    save_dir = increment_path(Path(project) / name, exist_ok=exist_ok)  # increment run 파일이 있다면 run폴더/detect폴더/exp 파일이름이 동일한 파일이 있으면 뒤에 2,3,4 등을 붙여준다
    (save_dir / "labels" if save_txt else save_dir).mkdir(parents=True, exist_ok=True)  # make dir 디렉토리가 없다면 만들어라 

    # Load model
    device = select_device(device) # CPU, GPU 선택 
    model = DetectMultiBackend(weights, device=device, dnn=dnn, data=data, fp16=half) # weights= 만약 라벨링하고 학습을 마치면 best.pt
    stride, names, pt = model.stride, model.names, model.pt
    # stride는 파라미터(convolution 필터가 이동하는 단계 크기를 결정)
    # stride가 크면 한번에 많은 픽셀을 이동하므로 출력이 다운샘플링 된다.
    # stride가 작으면 한번에 많은 픽셀을 이동할 수 없고 작은 픽셀을 이동하므로 출력 해상도가 올라감
    # 실제로 stride값은 아키텍처와 특정 작업에 따라 설정되는 경우가 있음 
    # model.names는 객체 탐지 또는 분류 모델과 관련된 클래스 이름 또는 레이블 목록을 참조
    # 사전 훈련된 많은 모델에서 model.names에는 (ex. "개", "자동차", "트럭", "버스")등등 일반적인 개체 범주에 목록이 포함되어 있다.
    # model.pt는 Pytorch모델에 로드하면 저장된 가중치로 모델이 초기화되어 추론이난 추가 교육에 사용
    # 여기에는 학습된 신경망의 학습된 가중치와 아키텍처가 포함 
    
    imgsz = check_img_size(imgsz, s=stride)  # check image size 이미지 사이즈 
    
    # imgsz의 경우 매개변수 처리에 필요한 이미지 크기를 나타낸다. 즉 너비와 높이를 포함하는 단일 값(정사각형 이미지)이거나 튜플(직사각형 이미지)를 나타날 때 사용
    # s = stride 매개변수는 이미지를 처리할 때 단계 크기를 지정. 처리창(ex 컨볼루션 필터)
    # 이미지에서 수평 및 수직으로 이동하는 정도를 결정 위 내용을 다시 보면 스트라이드가 크면 다운샘플링 작으면 미세한 세부정보가 유지(단 처리속도가 현저히 떨어짐)
    
    # Dataloader
    bs = 1  # batch_size
    if webcam:
        view_img = check_imshow(warn=True)
        cudnn.benchmark = True # constant image size inference 그래픽카드 Cuda Core를 활성화 
        dataset = LoadStreams(source, img_size=imgsz, stride=stride, auto=pt, vid_stride=vid_stride)
        bs = len(dataset)
    elif screenshot:
        dataset = LoadScreenshots(source, img_size=imgsz, stride=stride, auto=pt)
    else:
        dataset = LoadImages(source, img_size=imgsz, stride=stride, auto=pt, vid_stride=vid_stride)
        # LoadImages 함수는 지정된 소스(디렉터리 또는 파일 경로)에서 이미지 세트를 로드
        # 비전 작업에서는 훈련, 검증 또는 테스트를 위해 이미지를 로드하여 데이터셋을 생성하는 것이 일반적
        # auto=pt는 매개변수 함수가 Pytorch 호환 데이터 로드(ex 이미지를 텐서로 변환)를 자동으로 처리
        
    vid_path, vid_writer = [None] * bs, [None] * bs
    # vid_path, vid_writer을 초기화 처리
    # vid_path는 [None] * bs bs는 배치 크기를 나타냄
    # vid_writer 위와 동일
    # 비디오를 일괄 처리할 때 비디오 파일 경로를 추적하기 위해 사용 

# Run inference
    model.warmup(imgsz=(1 if pt or model.triton else bs, 3, *imgsz))  # warmup
    # 사전 정의된 신경망 모델을 의미
    # .warmup()의 경우 초기화를 진행
    # imgsz의 경우 모델의 입력 이미지 크기를 지정, 너비와 높이를 포함하는 단일 값(정사각형의 이미지)이거나 튜플(직사각형의 이미지)
    # (1 if pt or model.triton else bs, 3, *imgsz) 세 가지 요소로 튜플 구성 
    # 첫 번째 요소 1은 배치 크기 
    # 두 번쨰 요소 3은 색상 채널의 수를 나타냄
    # 세 번째 요소 imgsz(너비와 높이)
    # 모델의 가중치를 초기화하거나 학습 속도를 조정하거나 훈련 전에 기타 필요한 설정을 수행하기 위함
    # 프레임워크(ex Pytorch, Tensorflow)에 따라 값이 달라짐
    
    # 변수 및 리스트 초기화
    seen, windows, dt = 0, [], (Profile(device=device), Profile(device=device), Profile(device=device))
    # seen 변수를 int 0으로 초기화
    # windows 리스트를 초기화 
    # dt 튜플을 (Profile 함수에 맞게 초기화)
    
    for path, im, im0s, vid_cap, s in dataset: 
        # path는 이미지 파일이나 비디오의 경로
        # im은 로드된 이미지(tensor)
        # im0s 전처리가 된 이미지 
        # vid_cap의 경우 비디오인지 아닌지 구분하기 위함
        # s는 dataset과 관련된 추가정보(ex 라벨, 메타데이터)
        # 객체감지, 분할 또는 분류를 위해 반복문을 실행 
        
        with dt[0]:  # 이미지 변환 정규화
            im = torch.from_numpy(im).to(model.device) # 이미지 데이터는 Pytorch 텐서(im)로 변환되어 지정된 GPU 또는 CPU로 이동
            im = im.half() if model.fp16 else im.float()  # uint8 to fp16/32 / 모델이 fp16을 사용하는 경우 이미지는 fp16형식으로 추가 변환 
            im /= 255  # 0 - 255 to 0.0 - 1.0 / 픽셀 값은 [0,255]에서 [0.0, 1.0]범위로 정규화 
            if len(im.shape) == 3:
                im = im[None]  # expand for batch dim
            if model.xml and im.shape[0] > 1:
                ims = torch.chunk(im, im.shape[0], 0)

        # Inference
        with dt[1]:
            visualize = increment_path(save_dir / Path(path).stem, mkdir=True) if visualize else False 
            if model.xml and im.shape[0] > 1:
                pred = None
                for image in ims:
                    if pred is None:
                        pred = model(image, augment=augment, visualize=visualize).unsqueeze(0)
                    else:
                        pred = torch.cat((pred, model(image, augment=augment, visualize=visualize).unsqueeze(0)), dim=0)
                pred = [pred, None]
            else:
                pred = model(im, augment=augment, visualize=visualize) # yolo 모델에 현재 이미지 또는 영상을 대입 
        # NMS 중복 탐지를 필터링하기 위해 적용
        with dt[2]:
            pred = non_max_suppression(pred, conf_thres, iou_thres, classes, agnostic_nms, max_det=max_det) # 신뢰값, IoU 임계값, 클래스 필터링과 같은 매개변수 적용 
            # 최종 탐지는 pred에 저장

    # Second-stage classifier (optional)
    # pred = utils.general.apply_classifier(pred, classifier_model, im, im0s)

    # Define the path for the CSV file
    csv_path = save_dir / "predictions.csv"

    # Create or append to the CSV file
    def write_to_csv(image_name, prediction, confidence):
        """Writes prediction data for an image to a CSV file, appending if the file exists."""
        data = {"Image Name": image_name, "Prediction": prediction, "Confidence": confidence}
        with open(csv_path, mode="a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=data.keys())
            if not csv_path.is_file():
                writer.writeheader()
            writer.writerow(data)

        # Process predictions 객체 탐지 프로세스 
        for i, det in enumerate(pred):  # per image 여기서 부터 실제 인식 계산이 실행됨 
            # 반복하는 동안 해당 인덱스를 추적(인덱스-값) 열거 객체를 반환
            
            seen += 1 # seen이라는 변수를 우선 1로 증가시킴 
            if webcam:  # batch_size >= 1
                p, im0, frame = path[i], im0s[i].copy(), dataset.count # p에 path[i]를 대입, im0에 im0s.copy() 대입, frame에 getattr(data, 'frame',0)을 대입
                s += f"{i}: " # s(total 지역 크기)에 str i 값을 대입 
            else:
                p, im0, frame = path, im0s.copy(), getattr(dataset, "frame", 0) 
            
            # p에 path값이 할당됨 webcam
            # im0 im0s의 복사본이 할당됨. 원본 이미지를 표현 
            # frame getattr(dataset, "frame", 0)에서 얻은 값이 할당 dataset에 'frame'이라는 속성이 있으면 frame에 할당
            # 전반적으로 루프 내에서 추가 처리를 위해 필요한 변수를 준비
            list_x1 = []
            list_num = []
            p = Path(p)  # to Path 경로
            save_path = str(save_dir / p.name)  # im.jpg
            # p.name은 원본 파일명 save_dir은 경로 
            txt_path = str(save_dir / "labels" / p.stem) + ("" if dataset.mode == "image" else f"_{frame}")  # im.txt 사용하지 않음 
            
            # 라벨 정보(경계상자 좌표 및 클래스 라벨)가 저장된 경로를 구성
            # p에는 원본 이미지 파일의 경로
            # p.stem 경로에서 파일이름(확장자 제외)을 추출
            # dataset.mode는 이미지가 아닌 경우에 접미사(프레임 번호 기준)가 추가 
            # save_dir이 /results/이고, p.stem이 'my_image'이고, dataset.mode가 'image'인 경우 txt_path는 "result/labels/my_images.txt"가 됨.
            
            s += "%gx%g " % im.shape[2:] 
            # im.shape[2:] 이미지의 너비와 높이에 해당하는 모댱 튜플의 마지막 두 요소를 추출 
            # ex 이미지 크기가 640(너비) x 480(높이)인 경우 640x480을 포함하도록 s에 대입 
            
            gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh torch.tensor(im0.shape)에 높이 넓이 색을 가져와서 gn에 대입
           
            # 정규화 이득 계산
            # im0.shape 원본 이미지의 모양을 튜플로 반환 컬러이미지의 경우 일반적으로
            # 높이, 너비, 색상 채널수(ex RGB)의 3차원
            # 첫 번째 요소(1)은 이미지의 너비에 해당
            # 두 번째 요소(0)은 이미지의 높이에 해당
            # 정규화를 위해 세 번쨰와 네 번쨰 요소(1과 0)을 반복
            # 정규화 gn은 결과 gn 텐서의 정규화를 위한 정렬(이때 정렬에 너비와 높이를 포함)
            # 즉 경계 상자 좌표를 모델의 출력 크기에서 원본 이미지 크기로 조정하는데 사용 
            
            imc = im0.copy() if save_crop else im0  # for save_crop im0.copy()에서 온 값을 crop() 해라
            # save_crop args가 True이면 imc는 원본 이미지 복사
            # save_crop False이면 imc는 원본 이미지와 동일해서 복사를 하지 않음 
           
            annotator = Annotator(im0, line_width=line_thickness, example=str(names)) # im0은 이미지 정보를 가지고 있음, line_width = line_thickness box 선 굵기는 1, 인식된 name
            
            # 경계 상자 레이블과 시각적 주석을 이미지에 추가하기 위한 주석 개체를 초기화
            # im0 원본 이미지 데이터
            # line_width는 경계 상자 및 주석을 그리는데 사용 (선의 두께를 지정해서)
            # ex run/detect/exp에 이미지를 보면 person, dog 글이 적혀 있는 것을 볼 수 있음  
            
            count = 0 
            # 위의 내용은 웹캠인지 아니지 구분하고 경로 가져오고, 이미지의 크기 알아내고, crop을 활성화하고, 박스 선 굵기 정하고,
            # count에 0을 대입 
            
            if len(det): # det이 인식 이미지의 내용들을 거의 포함하고 있는 변수 
                # Rescale boxes from img_size to im0 size
                global global_list_num 
                det[:, :4] = scale_boxes(im.shape[2:], det[:, :4], im0.shape).round() # 이미지를 det의 return되어오는 값을 잘라라 
                # im.shape[2:]의 경우 처리된 이미지(im)의 크기(폭과 높이)를 추출. im의 모양은 (batch_size, 채널, 높이,너비)형식
                # det[:,:4] det의 처음 4개 열을 선택. 이러한 열은 모델에서 예측한 경계 상자 좌표(x_min.y_min,x_max,y_max)
                # im0.shape은 원본 이미지(im0)의 모양을 나타내며 일반적으로 형식(높이, 너비, 채널)을 갖는다.
                # scale_coords() 처리된 이미지 크기에서 원래 이미지 크기로 경계 상자 좌표의 크기를 조정하고 경계 상자가 원본 이미지와 올바르게 정렬되도록 함.
                # .round()는 결과 좌표의 유효한 픽셀 위치와 일치하는지 확인하기 위한 정수로 반올림 
                # 즉 이 코드 줄은 원본 이미지의 크기와 일치하도록 경계 상자 좌표를 조정하여 정확한 시각화 및 주석을 처리 

                # Print results
                for c in det[:, 5].unique(): # 해당 열에 있는 고유 값(class 라벨)를 반환. 라벨이란 모델을 통과시켜서 나온 값 
                    n = (det[:, 5] == c).sum()  # detections per class 각 고유 클래스 레이블(c)에 대해 해당 클래스와 관련된 탐지 수를 계산 
                    s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  # add to string 글씨를 입히는 과정
                    # .sum()은 마스크에 있는 True 값의 총 개수를 계산 
                    # {n} 현재 클래스 탐지 갯수
                    # {names[int(c)]} 클래스 이름(정수 클래스 라벨 c를 기반으로 이름 목록에서 검색)
                    # {'s' * (n > 1)} 감지가 여러 개(둘 이상) 있는 경우 클래스 이름에 's'를 추가
                    # 즉 검색된 클래스에 대한 정보와 해당 클래스의 개수를 문자열 s에 축적

                # Write results
                for *xyxy, conf, cls in reversed(det):
                    # xyxy는 각 감지에서 경계 상자 좌표(x_min, y_min, x_max, y_max)를 감지
                    # conf는 탐지와 관련된 신뢰도 점수
                    # cls는 클래스 레이블 
                    # reversed(det) 감지를 역방향으로 감지 즉 순서를 반대로 바꿈 
                    # 루프가 마지막(가장 높은 신뢰도)부터 첫 번째(가장 낮은 신뢰도)까지 탐지를 처리한다는 뜻 
                    # 탐지에 대한 경계 상자 좌표, 신뢰도 점수 및 클래스 레이블에 역순으로 액세스
                    
                    c = int(cls)  # integer class
                    label = names[c] if hide_conf else f"{names[c]}"
                    confidence = float(conf)
                    confidence_str = f"{confidence:.2f}"

                    if save_csv:
                        write_to_csv(p.name, label, confidence_str)

                    if save_txt:  # Write to file
                        xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn).view(-1).tolist()  # normalized xywh
                        line = (cls, *xywh, conf) if save_conf else (cls, *xywh)  # label format
                        with open(f"{txt_path}.txt", "a") as f:
                            f.write(("%g " * len(line)).rstrip() % line + "\n")

                    if save_img or save_crop or view_img:  # Add bbox to image
                        c = int(cls)  # integer class
                        im_re_0 = annotator.result()
                        # x1 = int(xyxy[0].item())
                        # print("x1=",x1)
                        
                        label = None if hide_labels else (names[c] if hide_conf else f"{names[c]} {conf:.2f}")
                        
                        # save_img, save_crop 또는 view_img의 조건 or 셋 중 하나라도 참이면 밑의 내용을 실행
                        # 변수 c에는 cls 정수 값이 할당
                        # 변수 라벨은 다음 조건에 결정
                        # hide_labels가 True이면 레이블은 없음으로 설정
                        # hide_conf가 True이면 label은 클래스 인덱스 c에 해당하는 이름으로 설정
                        # 두 조건이 모두 충족되지 않으면 label에는 소수점 이하 두자리로 형식화된 신뢰도 값과 클래스 이름이 모두 포함   
                    
                        annotator.box_label(xyxy, label, color=colors(c, True))
                        nn = label
                       # print('nn',nn)
                        ny = nn.split()
                        if ny[0] == 'a1':
                            ny[0] = '가'
                        elif ny[0] == 'a2':
                            ny[0] = '나'
                        elif ny[0] == 'a3':
                            ny[0] = '다'
                        elif ny[0] == 'a4':
                            ny[0] = '라'
                        elif ny[0] == 'a5':
                            ny[0] = '마'
                        

                        elif ny[0] == 'a6':
                            ny[0] = '거'
                        elif ny[0] == 'a7':
                            ny[0] = '너'
                        elif ny[0] == 'a8':
                            ny[0] = '더'
                        elif ny[0] == 'a9':
                            ny[0] = '러'
                        elif ny[0] == 'a10':
                            ny[0] = '머'
                        elif ny[0] == 'a11':
                            ny[0] = '버'
                        elif ny[0] == 'a12':
                            ny[0] = '서'
                        elif ny[0] == 'a13':
                            ny[0] = '어'
                        elif ny[0] == 'a14':
                            ny[0] = '저'
                        

                        elif ny[0] == 'a15':
                            ny[0] = '고'
                        elif ny[0] == 'a16':
                            ny[0] = '노'
                        elif ny[0] == 'a17':
                            ny[0] = '도'
                        elif ny[0] == 'a18':
                            ny[0] = '로'
                        elif ny[0] == 'a19':
                            ny[0] = '모'
                        elif ny[0] == 'a20':
                            ny[0] = '보'
                        elif ny[0] == 'a21':
                            ny[0] = '소'
                        elif ny[0] == 'a22':
                            ny[0] = '오'
                        elif ny[0] == 'a23':
                            ny[0] = '조'
                      

                        elif ny[0] == 'a24':
                            ny[0] = '구'
                        elif ny[0] == 'a25':
                            ny[0] = '누'
                        elif ny[0] == 'a26':
                            ny[0] = '두'
                        elif ny[0] == 'a27':
                            ny[0] = '루'
                        elif ny[0] == 'a28':
                            ny[0] = '무'
                        elif ny[0] == 'a29':
                            ny[0] = '부'
                        elif ny[0] == 'a30':
                            ny[0] = '수'
                        elif ny[0] == 'a31':
                            ny[0] = '우'
                        elif ny[0] == 'a32':
                            ny[0] = '주'
                            
                        elif ny[0] == 'b1':
                            ny[0] = '아'
                        elif ny[0] == 'b2':
                            ny[0] = '바'
                        elif ny[0] == 'b3':
                            ny[0] = '사'
                        elif ny[0] == 'b4':
                            ny[0] = '자'
                        elif ny[0] == 'c1':
                            ny[0] = '배'
                        elif ny[0] == 'd1':
                            ny[0] = '하'
                        elif ny[0] == 'd2':
                            ny[0] = '허'
                        elif ny[0] == 'd3':
                            ny[0] = '호'
                        x1 = int(xyxy[0].item())
                        # y1 = int(xyxy[1].item())
                        # x2 = int(xyxy[2].item())
                        # y1 = int(xyxy[3].item())
                        list_x1.append(x1)
                        list_num.append(ny[0])
                    if save_crop:
                        save_one_box(xyxy, imc, file=save_dir / "crops" / names[c] / f"{p.stem}.jpg", BGR=True)
            for k in range(len(list_x1)):
                    for j in range(len(list_x1) - 1):
                        if list_x1[j] > list_x1[j + 1]:  # bounding box 좌표를 오름차순으로 정렬
                            list_x1[j], list_x1[j + 1] = list_x1[j + 1], list_x1[j]
                            list_num[j], list_num[j + 1] = list_num[j + 1], list_num[j]
            list_numm = "".join(list_num)
            list_num_len = len(list_numm)
                #print("list_num",list_num)   
                    
            if ((list_numm[0] == '0' or list_numm[0] == '1' or list_numm[0] == '2' or list_numm[0] == '3' or
                    list_numm[0] == '4' or list_numm[0] == '5' or list_numm[0] == '6' or list_numm[0] == '7' or
                    list_numm[0] == '8' or list_numm[0] == '9') and
                    (list_numm[1] == '0' or list_numm[1] == '1' or list_numm[1] == '2' or list_numm[1] == '3' or
                    list_numm[1] == '4' or list_numm[1] == '5' or list_numm[1] == '6' or list_numm[1] == '7' or
                    list_numm[1] == '8' or list_numm[1] == '9') and
                    (list_numm[2] == '가' or list_numm[2] == '나' or list_numm[2] == '다' or list_numm[2] == '라' or
                    list_numm[2] == '마' or list_numm[2] == '바' or list_numm[2] == '사' or list_numm[2] == '아' or
                    list_numm[2] == '자' or list_numm[2] == '하' or list_numm[2] == '거' or list_numm[2] == '너' or
                    list_numm[2] == '더' or list_numm[2] == '러' or list_numm[2] == '머' or list_numm[2] == '버' or
                    list_numm[2] == '서' or list_numm[2] == '어' or list_numm[2] == '저' or list_numm[2] == '허' or
                    list_numm[2] == '고' or list_numm[2] == '노' or list_numm[2] == '도' or list_numm[2] == '로' or
                    list_numm[2] == '모' or list_numm[2] == '보' or list_numm[2] == '소' or list_numm[2] == '오' or
                    list_numm[2] == '조' or list_numm[2] == '호' or list_numm[2] == '구' or list_numm[2] == '누' or
                    list_numm[2] == '두' or list_numm[2] == '루' or list_numm[2] == '무' or list_numm[2] == '부' or
                    list_numm[2] == '수' or list_numm[2] == '우' or list_numm[2] == '주') and
                    (list_numm[3] == '0' or list_numm[3] == '1' or list_numm[3] == '2' or list_numm[3] == '3' or
                    list_numm[3] == '4' or list_numm[3] == '5' or list_numm[3] == '6' or list_numm[3] == '7' or
                    list_numm[3] == '8' or list_numm[3] == '9') and
                    (list_numm[4] == '0' or list_numm[4] == '1' or list_numm[4] == '2' or list_numm[4] == '3' or
                    list_numm[4] == '4' or list_numm[4] == '5' or list_numm[4] == '6' or list_numm[4] == '7' or
                    list_numm[4] == '8' or list_numm[4] == '9') and
                    (list_numm[5] == '0' or list_numm[5] == '1' or list_numm[5] == '2' or list_numm[5] == '3' or
                    list_numm[5] == '4' or list_numm[5] == '5' or list_numm[5] == '6' or list_numm[5] == '7' or
                    list_numm[5] == '8' or list_numm[5] == '9') and
                    (list_numm[6] == '0' or list_numm[6] == '1' or list_numm[6] == '2' or list_numm[6] == '3' or
                    list_numm[6] == '4' or list_numm[6] == '5' or list_numm[6] == '6' or list_numm[6] == '7' or
                    list_numm[6] == '8' or list_numm[6] == '9') and
                    (list_num_len == 7 or list_num_len == 8 or list_num_len == 9)):
                    
                        global_list_num = list_numm
                #print("global4=", global_list_num)

            elif ((list_numm[0] == '0' or list_numm[0] == '1' or list_numm[0] == '2' or list_numm[0] == '3' or
                    list_numm[0] == '4' or list_numm[0] == '5' or list_numm[0] == '6' or list_numm[0] == '7' or
                    list_numm[0] == '8' or list_numm[0] == '9') and
                    (list_numm[1] == '0' or list_numm[1] == '1' or list_numm[1] == '2' or list_numm[1] == '3' or
                    list_numm[1] == '4' or list_numm[1] == '5' or list_numm[1] == '6' or list_numm[1] == '7' or
                    list_numm[1] == '8' or list_numm[1] == '9') and
                    (list_numm[2] == '0' or list_numm[2] == '1' or list_numm[2] == '2' or list_numm[2] == '3' or
                    list_numm[2] == '4' or list_numm[2] == '5' or list_numm[2] == '6' or list_numm[2] == '7' or
                    list_numm[2] == '8' or list_numm[2] == '9') and
                    (list_numm[3] == '가' or list_numm[3] == '나' or list_numm[3] == '다' or list_numm[3] == '라' or
                    list_numm[3] == '마' or list_numm[3] == '바' or list_numm[3] == '사' or list_numm[3] == '아' or
                    list_numm[3] == '자' or list_numm[3] == '하' or list_numm[3] == '거' or list_numm[3] == '너' or
                    list_numm[3] == '더' or list_numm[3] == '러' or list_numm[3] == '머' or list_numm[3] == '버' or
                    list_numm[3] == '서' or list_numm[3] == '어' or list_numm[3] == '저' or list_numm[3] == '허' or
                    list_numm[3] == '고' or list_numm[3] == '노' or list_numm[3] == '도' or list_numm[3] == '로' or
                    list_numm[3] == '모' or list_numm[3] == '보' or list_numm[3] == '소' or list_numm[3] == '오' or
                    list_numm[3] == '조' or list_numm[3] == '호' or list_numm[3] == '구' or list_numm[3] == '누' or
                    list_numm[3] == '두' or list_numm[3] == '루' or list_numm[3] == '무' or list_numm[3] == '부' or
                    list_numm[3] == '수' or list_numm[3] == '우' or list_numm[3] == '주') and
                    (list_numm[4] == '0' or list_numm[4] == '1' or list_numm[4] == '2' or list_numm[4] == '3' or
                    list_numm[4] == '4' or list_numm[4] == '5' or list_numm[4] == '6' or list_numm[4] == '7' or
                    list_numm[4] == '8' or list_numm[4] == '9') and
                    (list_numm[5] == '0' or list_numm[5] == '1' or list_numm[5] == '2' or list_numm[5] == '3' or
                    list_numm[5] == '4' or list_numm[5] == '5' or list_numm[5] == '6' or list_numm[5] == '7' or
                    list_numm[5] == '8' or list_numm[5] == '9') and
                    (list_numm[6] == '0' or list_numm[6] == '1' or list_numm[6] == '2' or list_numm[6] == '3' or
                    list_numm[6] == '4' or list_numm[6] == '5' or list_numm[6] == '6' or list_numm[6] == '7' or
                    list_numm[6] == '8' or list_numm[6] == '9') and
                    (list_numm[7] == '0' or list_numm[7] == '1' or list_numm[7] == '2' or list_numm[7] == '3' or
                    list_numm[7] == '4' or list_numm[7] == '5' or list_numm[7] == '6' or list_numm[7] == '7' or
                    list_numm[7] == '8' or list_numm[7] == '9') and
                    (list_num_len == 7 or list_num_len == 8 or list_num_len == 9)):
                        global_list_num = list_numm
            print("p.stem",p.stem)
            print("p.name", p.name)
            print("label", label)
            print("global_list",global_list_num)

            # Stream results
            im0 = annotator.result() # 원래 이미지(im0)의 경계 상자와 레이블을 추가하는데 사용된 주석 개체를 호출
            # 결과는 시각적 주석(경계 상자 및 레이블)이 적용된 이밎
            # im0 주석이 달린 이미지로 업데이트되어 추가 처리 또는 저장 준비
            if view_img:
                if platform.system() == "Linux" and p not in windows:
                    windows.append(p)
                    cv2.namedWindow(str(p), cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)  # allow window resize (Linux)
                    cv2.resizeWindow(str(p), im0.shape[1], im0.shape[0])
                cv2.imshow(str(p), im0)
                cv2.waitKey(1)  # 1 millisecond

            # Save results (image with detections)
            if save_img:
                if dataset.mode == "image":
                    cv2.imwrite(save_path, im0)
                else:  # 'video' or 'stream'
                    if vid_path[i] != save_path:  # new video
                        vid_path[i] = save_path
                        if isinstance(vid_writer[i], cv2.VideoWriter):
                            vid_writer[i].release()  # release previous video writer
                        if vid_cap:  # video
                            fps = vid_cap.get(cv2.CAP_PROP_FPS)
                            w = int(vid_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                            h = int(vid_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                        else:  # stream
                            fps, w, h = 30, im0.shape[1], im0.shape[0]
                        save_path = str(Path(save_path).with_suffix(".mp4"))  # force *.mp4 suffix on results videos
                        vid_writer[i] = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))
                    vid_writer[i].write(im0)

        # Print time (inference-only)
        LOGGER.info(f"{s}{'' if len(det) else '(no detections), '}{dt[1].dt * 1E3:.1f}ms")

    # Print results
    t = tuple(x.t / seen * 1e3 for x in dt)  # speeds per image
    LOGGER.info(f"Speed: %.1fms pre-process, %.1fms inference, %.1fms NMS per image at shape {(1, 3, *imgsz)}" % t)
    if save_txt or save_img:
        s = f"\n{len(list(save_dir.glob('labels/*.txt')))} labels saved to {save_dir / 'labels'}" if save_txt else ""
        LOGGER.info(f"Results saved to {colorstr('bold', save_dir)}{s}")
    if update:
        strip_optimizer(weights[0])  # update model (to fix SourceChangeWarning)


def parse_opt():
    """Parses command-line arguments for YOLOv5 detection, setting inference options and model configurations."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--weights", nargs="+", type=str, default=ROOT / "yolov5s.pt", help="model path or triton URL") # yolo 모델 선정
    parser.add_argument("--source", type=str, default=ROOT / "data/images", help="file/dir/URL/glob/screen/0(webcam)") # 학습 데이터 read 경로
    parser.add_argument("--data", type=str, default=ROOT / "data/coco128.yaml", help="(optional) dataset.yaml path") # class 경로 및 파일 
    parser.add_argument("--imgsz", "--img", "--img-size", nargs="+", type=int, default=[640], help="inference size h,w") # 학습 사이즈 얼마로 줄거냐
    parser.add_argument("--conf-thres", type=float, default=0.5, help="confidence threshold") # 인식률 설정
    parser.add_argument("--iou-thres", type=float, default=0.5, help="NMS IoU threshold") # 인식률 설정
    parser.add_argument("--max-det", type=int, default=1000, help="maximum detections per image") # 이미지 몇 장까지
    parser.add_argument("--device", default="", help="cuda device, i.e. 0 or 0,1,2,3 or cpu") # cpu 혹은 gpu 사용할지 설정 
    parser.add_argument("--view-img", action="store_true", help="show results") # 이미지 view 
    parser.add_argument("--save-txt", action="store_true", help="save results to *.txt")
    parser.add_argument("--save-csv", action="store_true", help="save results in CSV format")
    parser.add_argument("--save-conf", action="store_true", help="save confidences in --save-txt labels")
    parser.add_argument("--save-crop", action="store_true", help="save cropped prediction boxes") # Crop box 설정 
    parser.add_argument("--nosave", action="store_true", help="do not save images/videos") # video 관련
    parser.add_argument("--classes", nargs="+", type=int, help="filter by class: --classes 0, or --classes 0 2 3")
    parser.add_argument("--agnostic-nms", action="store_true", help="class-agnostic NMS")
    parser.add_argument("--augment", action="store_true", help="augmented inference")
    parser.add_argument("--visualize", action="store_true", help="visualize features")
    parser.add_argument("--update", action="store_true", help="update all models")
    parser.add_argument("--project", default=ROOT / "runs/detect", help="save results to project/name") # 인식 데이터 결과가 저장되는 곳
    parser.add_argument("--name", default="exp", help="save results to project/name")
    parser.add_argument("--exist-ok", action="store_true", help="existing project/name ok, do not increment")
    parser.add_argument("--line-thickness", default=1, type=int, help="bounding box thickness (pixels)") # box 굵기
    parser.add_argument("--hide-labels", default=False, action="store_true", help="hide labels")
    parser.add_argument("--hide-conf", default=False, action="store_true", help="hide confidences")
    parser.add_argument("--half", action="store_true", help="use FP16 half-precision inference")
    parser.add_argument("--dnn", action="store_true", help="use OpenCV DNN for ONNX inference")
    parser.add_argument("--vid-stride", type=int, default=1, help="video frame-rate stride")
    opt = parser.parse_args()
    opt.imgsz *= 2 if len(opt.imgsz) == 1 else 1  # expand
    print_args(vars(opt))
    return opt


def main(opt):
    """Executes YOLOv5 model inference with given options, checking requirements before running the model."""
    check_requirements(ROOT / "requirements.txt", exclude=("tensorboard", "thop"))
    run(**vars(opt))


if __name__ == "__main__":
    opt = parse_opt()
    main(opt)
