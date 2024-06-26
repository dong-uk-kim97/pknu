# YOLOv5 🚀 by Ultralytics, AGPL-3.0 license
# print() 사용해서 디버깅 많이 해보기
"""
Run YOLOv5 detection inference on images, videos, directories, globs, YouTube, webcam, streams, etc.

Usage - sources:
    $ python detect.py --weights yolov5s.pt --source 0                               # webcam  // weights는 직접 학습한 모델 또는 yolo가 기본으로 제공해주는 모델의 종류(yolov5s가 여기에 해당함. ),
                                                                                               --source는 어떤 종류의 인식을 사용할건지 정함.
                                                     img.jpg                         # image
                                                     vid.mp4                         # video
                                                     screen                          # screenshot
                                                     path/                           # directory
                                                     list.txt                        # list of images
                                                     list.streams                    # list of streams
                                                     'path/*.jpg'                    # glob
                                                     'https://youtu.be/LNwODJXcvt4'  # YouTube
                                                     'rtsp://example.com/media.mp4'  # RTSP, RTMP, HTTP stream //카메라 영상을 접속해서 인식하기 위한 구문
source 별 이미지,동영상,RTSP 등을 선택해서 사용                                                

모델을 선정하게끔 속도를 빠르게 하고 싶으면 인식률은 조금 낮아도 yolov5s /속도는 느려도 인식률을 높이고 싶으면 yolov5x
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
기존 머신러닝 및 딥러닝은 텐서플로 , 케라스를 사용하였으나 Yolov5 부터는 pyTorch를 사용하여 성능을 최대화로 올림
                                 """

import argparse # cmd 동작을 시키기 위한 클래스 관리대상(epoch,batch_size,ir_initial)
import csv
import os
import platform
import sys
from pathlib import Path
import shutil
import torch #pytorch를 불러옴
#facebook에서 제공하는 딥러닝 도구로서,numpy와 효율적인 연동을 지원하는 편리한 도구이다.
# 구글에서는 tensorflow에서 개발
#tensorflow나 pytorch나 기본적인 data structure은 tensor 이다.
#tensor란 2차원 이상의 array이며, matrix,vector의 일반화된 객체이다.

# 일반화의 정의
# vector은 1차원 tensor이다.
# matrix는 2차원 tensor이다.
# 색을 나타내는 RGB는 3차원 tensor이다.
import torch.backends.cudnn as cudnn #학습 및 인식에는 두가지 방법이 있는데 CPU사용과 GPU(CUDA)사용으로  앞의 소스코드는 GPU가 있다면 불러와서 사용하겠다고 선언
global_list_num = None
FILE = Path(__file__).resolve() #현재 .py의 경로를 불러와서 FILE에 대입
ROOT = FILE.parents[0]  # YOLOv5 root directory 욜로 루트경로
if str(ROOT) not in sys.path: # 만약 ROOT가 없다면
    sys.path.append(str(ROOT))  # add ROOT to PATH 한번더 시도
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative ROOT를 찾았다면 경로와 cwd를 ROOT에 대입
count = 0
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


@smart_inference_mode()
def run(
    weights=ROOT / "best.pt",  # model path or triton URL 
    source=ROOT / "data/images",  # file/dir/URL/glob/screen/0(webcam) 인식을 시킬 폴더 경로
    data=ROOT / "data/coco128.yaml",  # dataset.yaml path 클래스가 정의되어 있는 파일
    imgsz=(640, 640),  # inference size (height, width)
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
    project=ROOT / "runs/detect",  # save results to project/name
    name="exp",  # save results to project/name
    exist_ok=False,  # existing project/name ok, do not increment / exist는 원하는 폴더에 파일이 있는지 없는지 알기 위한 구문
    line_thickness=3,  # bounding box thickness (pixels) 박스를 그릴 굵기
    hide_labels=False,  # hide labels
    hide_conf=False,  # hide confidences
    half=False,  # use FP16 half-precision inference
    dnn=False,  # use OpenCV DNN for ONNX inference
    vid_stride=1,  # video frame-rate stride
):
    source = str(source) #인식을 시킬 이미지들이 담겨 있는 경로
    save_img = not nosave and not source.endswith(".txt")  # save inference images 확장자를 구분하기 위한 구문
    is_file = Path(source).suffix[1:] in (IMG_FORMATS + VID_FORMATS) #img_formats + vid_formats값을 is_file의 처음부터 파일이 있는 끝까지 읽어와서 is_file에 대입
    is_url = source.lower().startswith(("rtsp://", "rtmp://", "http://", "https://"))
    webcam = source.isnumeric() or source.endswith(".streams") or (is_url and not is_file)
    screenshot = source.lower().startswith("screen")
    if is_url and is_file:
        source = check_file(source)  # download

    # Directories
    save_dir = increment_path(Path(project) / name, exist_ok=exist_ok)  # increment run 파일이 있다면
    (save_dir / "labels" if save_txt else save_dir).mkdir(parents=True, exist_ok=True)  # make dir 디렉토리가 없다면 만들어라

    # Load model
    device = select_device(device) #모델을 불러와 device에 대입
    model = DetectMultiBackend(weights, device=device, dnn=dnn, data=data, fp16=half) #weights =  만약 라벨링하고 학습을 마치면 best.pt
    stride, names, pt = model.stride, model.names, model.pt
    imgsz = check_img_size(imgsz, s=stride)  # check image size 이미지 사이즈

    # Dataloader
    bs = 1  # batch_size
    if webcam:
        view_img = check_imshow(warn=True)
        dataset = LoadStreams(source, img_size=imgsz, stride=stride, auto=pt, vid_stride=vid_stride)
        bs = len(dataset)
    elif screenshot:
        dataset = LoadScreenshots(source, img_size=imgsz, stride=stride, auto=pt)
    else:
        dataset = LoadImages(source, img_size=imgsz, stride=stride, auto=pt, vid_stride=vid_stride)
    vid_path, vid_writer = [None] * bs, [None] * bs

    # Run inference
    model.warmup(imgsz=(1 if pt or model.triton else bs, 3, *imgsz))  # warmup
    seen, windows, dt = 0, [], (Profile(device=device), Profile(device=device), Profile(device=device))
    for path, im, im0s, vid_cap, s in dataset: #path = 경로,im = 학습할 이미지,im0s = 인식이 되어져 나온 이미지, vid_cap = 비디오 또는 이미지, s = total 지역 크기
        with dt[0]:
            im = torch.from_numpy(im).to(model.device)
            im = im.half() if model.fp16 else im.float()  # uint8 to fp16/32
            im /= 255  # 0 - 255 to 0.0 - 1.0
            if len(im.shape) == 3:
                im = im[None]  # expand for batch dim
            if model.xml and im.shape[0] > 1:
                ims = torch.chunk(im, im.shape[0], 0)

        # Inference
        with dt[1]:
            visualize = increment_path(save_dir / Path(path).stem, mkdir=True) if visualize else False #새로운 경로를 만듦
            if model.xml and im.shape[0] > 1:
                pred = None
                for image in ims:
                    if pred is None:
                        pred = model(image, augment=augment, visualize=visualize).unsqueeze(0) #yolo 모델에 현재 이미지 또는 영상을 대입
                    else:
                        pred = torch.cat((pred, model(image, augment=augment, visualize=visualize).unsqueeze(0)), dim=0)
                pred = [pred, None]
            else:
                pred = model(im, augment=augment, visualize=visualize)
        # NMS
        with dt[2]:
            pred = non_max_suppression(pred, conf_thres, iou_thres, classes, agnostic_nms, max_det=max_det) #classes yaml 파일의 class를 읽어 옴

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

        # Process predictions
        for i, det in enumerate(pred):  # per image 여기서부터 실제 인식 계산이 실행 됨. 
            seen += 1 #seen이라는 변수를 우선 1로 증가 시킴
            if webcam:  # batch_size >= 1 webcam이 참이면
                p, im0, frame = path[i], im0s[i].copy(), dataset.count # p에 path[i]를 대입,im0에 im0s.copy() 대입, frame에 getattr(dataset,'frame',0)을 대입
                s += f"{i}: "
            else:
                p, im0, frame = path, im0s.copy(), getattr(dataset, "frame", 0)

            p = Path(p)  # to Path
            save_path = str(save_dir / p.name)  # im.jpg
            txt_path = str(save_dir / "labels" / p.stem) + ("" if dataset.mode == "image" else f"_{frame}")  # im.txt 사용하지 않음(시간이 많이 소요)
            s += "%gx%g " % im.shape[2:]  # print string # shape은 높이 넓이 색깔을 return 해준다.
            gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh torch.tensor(im0.shape)에 높이 넓이 색을 가져와서 gn에 대입
            imc = im0.copy() if save_crop else im0  # for save_crop im0.copy()에서 온 값을 crop(잘라라)해라
            annotator = Annotator(im0, line_width=line_thickness, example=str(names)) #im0 은 이미지 정보를 가지고 있음, line_width=line_thickness box 선 굵기는 1 인식된 name
            # 위의 내용은 웹캠인지 아닌지 구분하고 경로 가져오고, 이미지의 크기 알아내고, crop을 활성화 하고, 박스 선 굵기 정하고, count에 0을 대입
            list_x1 = []
            list_num = []
            if len(det): #det 인식 이미지의 내용들을 거의 포함하고 있는 변수
                # Rescale boxes from img_size to im0 size
                global global_list_num , count 
                det[:, :4] = scale_boxes(im.shape[2:], det[:, :4], im0.shape).round() # 이미지의 det의 return 되어오는 값을 잘라라 
                
                # Print results
                for c in det[:, 5].unique():
                    n = (det[:, 5] == c).sum()  # detections per class yaml 파일의 classe name을 가져와서 대입
                    s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  # add to string 글씨를 업하는 과정

                # Write results
                for *xyxy, conf, cls in reversed(det):
                  
                 
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
                        # im_re_0 = save_one_box(xyxy, imc, file=save_dir / 'crops' / f'{p.stem}.jpg',
                        #                                BGR=True)
                        # # cv2.imwrite("C:\\Wiirow\\Deep\\number_recognition\\yolov5_master\\yolov5_master\\data\\images\\" + str(p.stem) + "+" + str(count) + + ".jpg", im_re_0)
                        # shutil.move(os.path.join(os.path.abspath(save_dir)+'/crops/'+str(p.stem)+".jpg"), "C:\\Users\\Administrator\\anaconda3\\envs\\yolo\\yolov5-master-number\\yolov5-master\\data\\images33\\" )
                        label = None if hide_labels else (names[c] if hide_conf else f"{names[c]} {conf:.2f}")
                        annotator.box_label(xyxy, label, color=colors(c, True))
                        
                        # if x1>0 and x1 <200:
                        #     print("1차선입니다")
                        # elif x1 >=200:
                        #     print("2차선입니다.")
                #####################################################
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
                        save_one_box(xyxy, imc, file=save_dir / 'crops' / names[c] / f'{p.stem}.jpg', BGR=True)
                        #print("save_crop_test")  # 동작안함
            # if list_num == 'c3':
            # print("good")

                    # if list_num ==
                    # 인식된 숫자들의 bounding box 좌표를 오름차순으로 정렬 per frame -> 버스 번호 인식
                for k in range(len(list_x1)): # 위에서 역순으로 되어 있고 순서대로 인식되지 않은 문자 및 숫자를 오름차순으로 정렬 
                    for j in range(len(list_x1) - 1):
                        if list_x1[j] > list_x1[j + 1]:  # bounding box 좌표를 오름차순으로 정렬
                            list_x1[j], list_x1[j + 1] = list_x1[j + 1], list_x1[j]
                            list_num[j], list_num[j + 1] = list_num[j + 1], list_num[j]
                list_numm = "".join(list_num)
                list_num_len = len(list_numm)
                #print("list_num",list_num)   
                if (len(list_numm) > 6 and 
                    (list_numm[0] in '0123456789') and
                    (list_numm[1] in '0123456789') and
                    (list_numm[2] in '가나다라마바사아자하거너더러머버서어저허고노도로모보소오조호구누두루무부수우주') and
                    (list_numm[3] in '0123456789') and
                    (list_numm[4] in '0123456789') and
                    (list_numm[5] in '0123456789') and
                    (list_numm[6] in '0123456789') and
                    (list_num_len in [7, 8, 9])):
                        global_list_num = list_numm
                        # print("car_number = ",list_numm[0],list_numm[1],list_numm[2],list_numm[3],list_numm[4],list_numm[5],list_numm[6],end="")

                elif (len(list_numm) > 7 and 
                    (list_numm[0] in '0123456789') and
                    (list_numm[1] in '0123456789') and
                    (list_numm[2] in '0123456789') and
                    (list_numm[3] in '가나다라마바사아자하거너더러머버서어저허고노도로모보소오조호구누두루무부수우주') and
                    (list_numm[4] in '0123456789') and
                    (list_numm[5] in '0123456789') and
                    (list_numm[6] in '0123456789') and
                    (list_numm[7] in '0123456789') and
                    (list_num_len in [7, 8, 9])):
                        global_list_num = list_numm  
                        # print("car_number = ", list_numm[0],list_numm[1],list_numm[2],list_numm[3],list_numm[4],list_numm[5],list_numm[6],list_numm[7],end="")
                # if ((list_numm[0] == '0' or list_numm[0] == '1' or list_numm[0] == '2' or list_numm[0] == '3' or
                #         list_numm[0] == '4' or list_numm[0] == '5' or list_numm[0] == '6' or list_numm[0] == '7' or
                #         list_numm[0] == '8' or list_numm[0] == '9') and
                #         (list_numm[1] == '0' or list_numm[1] == '1' or list_numm[1] == '2' or list_numm[1] == '3' or
                #         list_numm[1] == '4' or list_numm[1] == '5' or list_numm[1] == '6' or list_numm[1] == '7' or
                #         list_numm[1] == '8' or list_numm[1] == '9') and
                #         (list_numm[2] == '가' or list_numm[2] == '나' or list_numm[2] == '다' or list_numm[2] == '라' or
                #         list_numm[2] == '마' or list_numm[2] == '바' or list_numm[2] == '사' or list_numm[2] == '아' or
                #         list_numm[2] == '자' or list_numm[2] == '하' or list_numm[2] == '거' or list_numm[2] == '너' or
                #         list_numm[2] == '더' or list_numm[2] == '러' or list_numm[2] == '머' or list_numm[2] == '버' or
                #         list_numm[2] == '서' or list_numm[2] == '어' or list_numm[2] == '저' or list_numm[2] == '허' or
                #         list_numm[2] == '고' or list_numm[2] == '노' or list_numm[2] == '도' or list_numm[2] == '로' or
                #         list_numm[2] == '모' or list_numm[2] == '보' or list_numm[2] == '소' or list_numm[2] == '오' or
                #         list_numm[2] == '조' or list_numm[2] == '호' or list_numm[2] == '구' or list_numm[2] == '누' or
                #         list_numm[2] == '두' or list_numm[2] == '루' or list_numm[2] == '무' or list_numm[2] == '부' or
                #         list_numm[2] == '수' or list_numm[2] == '우' or list_numm[2] == '주') and
                #         (list_numm[3] == '0' or list_numm[3] == '1' or list_numm[3] == '2' or list_numm[3] == '3' or
                #         list_numm[3] == '4' or list_numm[3] == '5' or list_numm[3] == '6' or list_numm[3] == '7' or
                #         list_numm[3] == '8' or list_numm[3] == '9') and
                #         (list_numm[4] == '0' or list_numm[4] == '1' or list_numm[4] == '2' or list_numm[4] == '3' or
                #         list_numm[4] == '4' or list_numm[4] == '5' or list_numm[4] == '6' or list_numm[4] == '7' or
                #         list_numm[4] == '8' or list_numm[4] == '9') and
                #         (list_numm[5] == '0' or list_numm[5] == '1' or list_numm[5] == '2' or list_numm[5] == '3' or
                #         list_numm[5] == '4' or list_numm[5] == '5' or list_numm[5] == '6' or list_numm[5] == '7' or
                #         list_numm[5] == '8' or list_numm[5] == '9') and
                #         (list_numm[6] == '0' or list_numm[6] == '1' or list_numm[6] == '2' or list_numm[6] == '3' or
                #         list_numm[6] == '4' or list_numm[6] == '5' or list_numm[6] == '6' or list_numm[6] == '7' or
                #         list_numm[6] == '8' or list_numm[6] == '9') and
                #         (list_num_len == 7 or list_num_len == 8 or list_num_len == 9)):
                        
                #             global_list_num = list_numm
                            
                    #print("global4=", global_list_num)

                # elif ((list_numm[0] == '0' or list_numm[0] == '1' or list_numm[0] == '2' or list_numm[0] == '3' or
                #         list_numm[0] == '4' or list_numm[0] == '5' or list_numm[0] == '6' or list_numm[0] == '7' or
                #         list_numm[0] == '8' or list_numm[0] == '9') and
                #         (list_numm[1] == '0' or list_numm[1] == '1' or list_numm[1] == '2' or list_numm[1] == '3' or
                #         list_numm[1] == '4' or list_numm[1] == '5' or list_numm[1] == '6' or list_numm[1] == '7' or
                #         list_numm[1] == '8' or list_numm[1] == '9') and
                #         (list_numm[2] == '0' or list_numm[2] == '1' or list_numm[2] == '2' or list_numm[2] == '3' or
                #         list_numm[2] == '4' or list_numm[2] == '5' or list_numm[2] == '6' or list_numm[2] == '7' or
                #         list_numm[2] == '8' or list_numm[2] == '9') and
                #         (list_numm[3] == '가' or list_numm[3] == '나' or list_numm[3] == '다' or list_numm[3] == '라' or
                #         list_numm[3] == '마' or list_numm[3] == '바' or list_numm[3] == '사' or list_numm[3] == '아' or
                #         list_numm[3] == '자' or list_numm[3] == '하' or list_numm[3] == '거' or list_numm[3] == '너' or
                #         list_numm[3] == '더' or list_numm[3] == '러' or list_numm[3] == '머' or list_numm[3] == '버' or
                #         list_numm[3] == '서' or list_numm[3] == '어' or list_numm[3] == '저' or list_numm[3] == '허' or
                #         list_numm[3] == '고' or list_numm[3] == '노' or list_numm[3] == '도' or list_numm[3] == '로' or
                #         list_numm[3] == '모' or list_numm[3] == '보' or list_numm[3] == '소' or list_numm[3] == '오' or
                #         list_numm[3] == '조' or list_numm[3] == '호' or list_numm[3] == '구' or list_numm[3] == '누' or
                #         list_numm[3] == '두' or list_numm[3] == '루' or list_numm[3] == '무' or list_numm[3] == '부' or
                #         list_numm[3] == '수' or list_numm[3] == '우' or list_numm[3] == '주') and
                #         (list_numm[4] == '0' or list_numm[4] == '1' or list_numm[4] == '2' or list_numm[4] == '3' or
                #         list_numm[4] == '4' or list_numm[4] == '5' or list_numm[4] == '6' or list_numm[4] == '7' or
                #         list_numm[4] == '8' or list_numm[4] == '9') and
                #         (list_numm[5] == '0' or list_numm[5] == '1' or list_numm[5] == '2' or list_numm[5] == '3' or
                #         list_numm[5] == '4' or list_numm[5] == '5' or list_numm[5] == '6' or list_numm[5] == '7' or
                #         list_numm[5] == '8' or list_numm[5] == '9') and
                #         (list_numm[6] == '0' or list_numm[6] == '1' or list_numm[6] == '2' or list_numm[6] == '3' or
                #         list_numm[6] == '4' or list_numm[6] == '5' or list_numm[6] == '6' or list_numm[6] == '7' or
                #         list_numm[6] == '8' or list_numm[6] == '9') and
                #         (list_numm[7] == '0' or list_numm[7] == '1' or list_numm[7] == '2' or list_numm[7] == '3' or
                #         list_numm[7] == '4' or list_numm[7] == '5' or list_numm[7] == '6' or list_numm[7] == '7' or
                #         list_numm[7] == '8' or list_numm[7] == '9') and
                #         (list_num_len == 7 or list_num_len == 8 or list_num_len == 9)):
                #             global_list_num = list_numm
                            
                print("p.stem",p.stem)
                # print("p.name", p.name)
                # print("label", label)
                print("global_list",global_list_num)
                if p.stem == global_list_num:
                    count +=1
                elif "-" in p.stem:
                    a=p.stem.split("-")[0]
                    if a==global_list_num:
                        count +=1
                print(count)
                global_list_num = None
                

                            
                 #################################################3       
                   

            # Stream results
            im0 = annotator.result()
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
    parser.add_argument("--weights", nargs="+", type=str, default=ROOT / "best.pt", help="model path or triton URL") # yolo 모델 선정
    parser.add_argument("--source", type=str, default=ROOT / "data/images", help="file/dir/URL/glob/screen/0(webcam)") # 학습데이터read경로
    parser.add_argument("--data", type=str, default=ROOT / "data/coco128.yaml", help="(optional) dataset.yaml path") # class경로 및 파일
    parser.add_argument("--imgsz", "--img", "--img-size", nargs="+", type=int, default=[640], help="inference size h,w") # 학습사이즈 몇으로 설정?
    parser.add_argument("--conf-thres", type=float, default=0.4, help="confidence threshold") # 인식률 설정 기존 0.25 50=정수로 나옴
    parser.add_argument("--iou-thres", type=float, default=0.4, help="NMS IoU threshold") # 인식률 설정 ( 값 바꿔서 해보기 1: 100%의미) 기존 0.45
    parser.add_argument("--max-det", type=int, default=1000, help="maximum detections per image") # 이미지 최종 몇장까지
    parser.add_argument("--device", default="", help="cuda device, i.e. 0 or 0,1,2,3 or cpu") # cpu를 사용할지 cuda를 사용할지 결정
    # cpu를 써도 그렇게 느리다고 체감하지도 못함. 차량기준 팬티엄 골드스타로 사용했을 경우 시간당 2만 5천장 처리
    parser.add_argument("--view-img", action="store_true", help="show results") #view 이미지
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
    parser.add_argument("--hide-conf", default=True, action="store_true", help="hide confidences") ##default=True하면 정수로 나옴
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


if __name__ == "__main__": # <- 이게 없다면 다른 파일에서 실행할 때 실행 안됨
    opt = parse_opt()
    main(opt)
