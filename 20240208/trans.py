import cv2
import json
import glob

"""

목표 경로 = '/content/drive/MyDrive/flame_Driving/work_space/gun/annotation'
전체 json파일 들어있는 폴더

"""


class CollectLabel:

    """
    Takes in the path to COCO annotations and outputs YOLO annotations in multiple .txt files.
    COCO annotation are to be JSON formart as follows:
        "annotations":{
            "area":2304645,
            "id":1,
            "image_id":10,
            "category_id":4,
            "bbox":[
                0::704
                1:620
                2:1401
                3:1645
            ]
        }
        
    """

    def __init__(self, json_path):
        #self.img_folder = img_folder
        self.json_path = json_path        
        #self.img_path = img_path

    # def get_img_shape(self, img_path):
    #     img = cv2.imread(img_path)
    #     try:
    #         return img.shape
    #     except AttributeError:
    #         print('error!', img_path)
    #         return (None, None, None)
    


    def convert_labels(self, xmin, ymax, xmax, ymin):
        """
        Definition: Parses label files to extract label and bounding box
        coordinates. Converts (x1, y1, x1, y2) KITTI format to
        (x, y, width, height) normalized YOLO format.
        """

        # def sorting(l1, l2):
        #     if l1 > l2:
        #         lmax, lmin = l1, l2
        #         return lmax, lmin
        #     else:
        #         lmax, lmin = l2, l1
        #         return lmax, lmin

        size = (1024,1920,3)
        # xmax, xmin = sorting(x1, x2)
        # ymax, ymin = sorting(y1, y2)
        dw = 1./size[1]
        dh = 1./size[0]
        x = (xmin + xmax)/2.0
        y = (ymin + ymax)/2.0
        w = xmax - xmin
        h = ymax - ymin
        x = x*dw
        w = w*dw
        y = y*dh
        h = h*dh
        return (x,y,w,h)


    def convert(self,annotation_key='annotations',img_id='filename', detect_label='label',bbox='bbox'):
        all_files = glob.glob(self.json_path + '/*.json')
        for j in range(len(all_files)):
            json_path = all_files[j]
            data = json.load(open(json_path))

            # Enter directory to read JSON file
            #data = json.load(open(self.json_path))
            
            check_set = set()


            # Retrieve data
            for i in range(len(data[annotation_key])):

                # Get required data
                image_id = f'{data[img_id]}'
                # category_id = f'{data[annotation_key][i][cat_id]}'

                
                #detection_label = f'{data[annotation_key][i][detect_label]}'
                
                # traffic_light, traffic_sign, car_number, PTW, rider, face(필요없는 클래스) 제외
                temp = data[annotation_key][i][detect_label]

                if temp == 'vehicle':
                    temp = 0
                elif temp == 'pedestrian':
                    temp = 1
                elif temp == 'yellow_vehicle':
                    temp = 2
                elif temp == 'police':
                    temp = 3
                elif temp == 'movable_object':
                    temp = 4
                elif temp == 'fire':
                    temp = 5
                elif temp == 'animal':
                    temp = 6
                elif temp == 'emergency':
                    temp = 7
                # traffic_light, traffic_sign, car_number, ptw, rider, face에 대한 YOLO 좌표 변환값은 txt에 추가하지 않고 건너뛰게끔 하는 부분(최고 중요!!!!!!)
                elif temp == 'traffic_light' or temp == 'traffic_sign' or temp == 'car_number' or temp == 'ptw' or temp =='rider' or temp =='face':
                    continue  
                
                  
                bbox = data[annotation_key][i]['points']

                # # Retrieve image.
                # if self.img_folder == None:
                #     image_path = f'{image_id}.jpg'
                # else:
                #     image_path = f'./{self.img_folder}/{image_id}.jpg'


                # Convert the data
                # kitti_bbox = [bbox[0], bbox[1], bbox[2] + bbox[0], bbox[3] + bbox[1]]
                x = [] 
                for i in range(len(bbox)):
                    x.append(bbox[i][0])
                
                xmin = min(x)
                xmax = max(x)

                y = []
                for i in range(len(bbox)):
                    y.append(bbox[i][1])
                ymin = min(y)
                ymax = max(y)


                yolo_bbox = self.convert_labels(xmin, ymax, xmax, ymin)


                # Prepare for export
                
                filename = f'{image_id[:-4]}.txt'
                content =f"{temp} {yolo_bbox[0]} {yolo_bbox[1]} {yolo_bbox[2]} {yolo_bbox[3]}"

                filepath = '/content/drive/MyDrive/flame_Driving/work_space/gun/annotation/collect_label/'
                #filename.save(filepath)

                # Export 
                if image_id in check_set:
                    # Append to existing file as there can be more than one label in each image
                    file = open(filepath + filename, "a")
                    file.write("\n")
                    file.write(content)
                    file.close()

                elif image_id not in check_set:
                    check_set.add(image_id)
                    # Write files
                    file = open(filepath+filename, "w")
                    file.write(content)
                    file.close()


# To run in as a class
if __name__ == "__main__":
    
    CollectLabel(json_path='').convert()