import torch
import cv2
from numpy import random
import numpy as np
from urllib.request import urlopen
import threading
import time
import os
import pathlib
import sys
temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath
os.chdir(os.path.dirname(os.path.abspath(__file__)))

ip = '192.168.137.210'
stream = urlopen('http://' + ip + ':81/stream')
buffer = b''
urlopen('http://' + ip + "/action?go=speed70")

# YOLOv5 모델 정의
model = torch.hub.load('ultralytics/yolov5', 'custom', path='./ch07_Object_Detection/data/5th/best.pt', trust_repo=True)

yolo_state = "go"
thread_frame = None  
image_flag = 0
thread_image_flag = 0
car_state = "go"

def yolo_thread():
    global image_flag, thread_image_flag, frame, thread_frame, yolo_state
    while True:
        if image_flag == 1:
            thread_frame = frame.copy()  # 원본 프레임을 직접 조작하지 않기 위해 복사본 사용
            
            # 이미지를 모델에 입력
            results = model(thread_frame)
            
            # 객체 감지 결과 얻기
            detections = results.pandas().xyxy[0]
            
            if detections.empty:
                print("default go")
                yolo_state = "go"
                urlopen('http://' + ip + "/action?go=speed70")
            else:
                # 결과를 반복하며 객체 표시
                for _, detection in detections.iterrows():
                    x1, y1, x2, y2 = detection[['xmin', 'ymin', 'xmax', 'ymax']].astype(int).values
                    label = detection['name']
                    conf = detection['confidence']
                    
                    # print(x1,", ", x2, ", ", y1, ", ", y2)
                    if "person" in label and conf > 0.6:
                        print("person")
                        yolo_state = "stop"
                    elif ("bike" in label or "car" in label) and conf > 0.5:
                        print("obstacle")
                        if ((x2 - x1) > 150) or ((y2 - y1) > 150): #매우 근접하면 정지
                            print("stop state")
                            yolo_state = "stop"
                        elif ((x2 - x1) > 120) or ((y2 - y1) > 120): #어느정도 근접하면 천천히
                            print("slow state")
                            yolo_state = "go"
                            urlopen('http://' + ip + "/action?go=speed50")
                    elif "stop" in label and conf > 0.6:
                        print("stop")
                        if ((x2 - x1) > 120) or ((y2 - y1) > 120): #어느정도 근접하면 정지
                            print("stop state")
                            yolo_state = "stop"
                    elif "slow" in label and conf > 0.6:
                        print("slow")
                        if ((x2 - x1) > 120) or ((y2 - y1) > 120): #어느정도 근접하면 천천히
                            print("slow state")
                            yolo_state = "go"
                            urlopen('http://' + ip + "/action?go=speed50")
                    elif "Uturn" in label and conf > 0.6:
                        print("Uturn")
                        if ((x2 - x1) > 120) or ((y2 - y1) > 120): #어느정도 근접하면 유턴
                            print("Uturn state")
                            yolo_state = "Uturn"
                            urlopen('http://' + ip + "/action?go=speed80")
                    elif "left" in label and conf > 0.5 :
                        print("left detect") #
                        if ((x2 - x1) > 100) or ((y2 - y1) > 100): #어느정도 근접하면 4초동안 좌회전
                            print("left turn")
                            yolo_state = "left"
                            urlopen('http://' + ip + "/action?go=speed80")
                            urlopen('http://' + ip + "/action?go=left")
                            time.sleep(4) 
                            print("turn end")
                            urlopen('http://' + ip + "/action?go=forward")

                    
                    # 박스와 라벨 표시
                    color = np.random.randint(0, 256, size=3).tolist()  # 무작위 색상 선택
                    cv2.rectangle(thread_frame, (x1, y1), (x2, y2), color, 2)
                    cv2.putText(thread_frame, f'{label} {conf:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            
            thread_image_flag = 1
            image_flag = 0
        
        time.sleep(0.2)  # CPU 사용량을 줄이기 위해 작은 대기 시간 추가

# 데몬 스레드를 생성하고 시작합니다.
t1 = threading.Thread(target=yolo_thread)
t1.daemon = True 
t1.start()

def image_process_thread():
    global image_flag, car_state, yolo_state
    while True:
        if image_flag == 1:
            if car_state == "go" and yolo_state == "go":
                urlopen('http://' + ip + "/action?go=forward")
            elif car_state == "right" and yolo_state == "go":
                urlopen('http://' + ip + "/action?go=right")
            elif car_state == "left" and yolo_state == "go":
                urlopen('http://' + ip + "/action?go=left")
            elif car_state == "left" and yolo_state == "left":
                urlopen('http://' + ip + "/action?go=left")    
            elif yolo_state == "Uturn":
                urlopen('http://' + ip + "/action?go=turn_right")
            elif yolo_state == "stop":
                urlopen('http://' + ip + "/action?go=stop")
            image_flag = 0
            
# 데몬 스레드를 생성하고 시작합니다.
t2 = threading.Thread(target=image_process_thread)
t2.daemon = True 
t2.start()

while True:
    buffer += stream.read(4096)
    head = buffer.find(b'\xff\xd8')
    end = buffer.find(b'\xff\xd9')
    
    try: 
        if head > -1 and end > -1:
            jpg = buffer[head:end+2]
            buffer = buffer[end+2:]
            img = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_UNCHANGED)

            # 프레임 크기 조정
            frame = cv2.resize(img, (640, 480))

            height, width, _ = img.shape
            img = img[height // 2:height-30, 10:width-10]
            
            # 색상 필터링으로 검정색 선 추출
            lower_bound = np.array([0, 0, 0])
            upper_bound = np.array([255, 255, 80])
            mask = cv2.inRange(img, lower_bound, upper_bound)
            # cv2.imshow("mask", mask)
            
            # 무게 중심 계산
            M = cv2.moments(mask)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
            else:
                cX, cY = 0, 0
            
            # 무게 중심과 이미지 중앙의 거리 계산
            center_offset = width // 2 - cX

            # 디버그용 시각화
            # cv2.circle(img, (cX, cY), 10, (0, 255, 0), -1)
            # cv2.imshow("AI CAR Streaming", img)
            
            # 현재 무게중심 위치가 -50~50은 직진하도록 설계
            if center_offset < -70:
                #print(f"오른쪽/{car_state}")
                car_state = "right"
            
            elif center_offset > 70:
                #print(f"왼쪽/{car_state}")
                car_state = "left"
                
            else:
                #print(f"직진/{car_state}")
                car_state = "go"
            
                
            image_flag = 1

            # 쓰레드에서 이미지 처리가 완료되었으면
            if thread_image_flag == 1:
                # cv2.imshow('thread_frame', thread_frame)
                thread_image_flag = 0

            key = cv2.waitKey(1)
            if key == ord('q'):
                break

    except KeyboardInterrupt as e:
        print("KeyboardInterrupt")
        sys.exit()

    except Exception as e:
        print("에러:", str(e))
        pass

urlopen('http://' + ip + "/action?go=stop")
cv2.destroyAllWindows()