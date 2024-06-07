import torch
import cv2
from numpy import random
import numpy as np
from urllib.request import urlopen
import os
import pathlib
import threading
import time
temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath
os.chdir(os.path.dirname(os.path.abspath(__file__)))

ip = '192.168.137.91'
stream = urlopen('http://' + ip + ':81/stream')
buffer = b''
urlopen('http://' + ip + "/action?go=speed40")

# YOLOv5 모델 정의
model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt')

frame = None
frame_lock = threading.Lock()
stop_event = threading.Event()

def stream_receiver():
    global frame, buffer
    while not stop_event.is_set():
        buffer += stream.read(4096)
        head = buffer.find(b'\xff\xd8')
        end = buffer.find(b'\xff\xd9')

        if head > -1 and end > -1:
            jpg = buffer[head:end+2]
            buffer = buffer[end+2:]
            img = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
            with frame_lock:
                frame = cv2.resize(img, (640, 480))

def object_detection():
    global frame
    detection_interval = 0.3  # 0.3초 간격으로 객체 감지
    last_detection_time = 0

    while not stop_event.is_set():
        with frame_lock:
            if frame is not None:
                current_frame = frame.copy()
            else:
                current_frame = None
        
        if current_frame is not None and time.time() - last_detection_time >= detection_interval:
            results = model(current_frame)
            detections = results.pandas().xyxy[0]
            last_detection_time = time.time()

            if not detections.empty:
                # 결과를 반복하며 객체 표시
                for _, detection in detections.iterrows():
                    x1, y1, x2, y2 = detection[['xmin', 'ymin', 'xmax', 'ymax']].astype(int).values
                    label = detection['name']
                    conf = detection['confidence']

                    # 박스와 라벨 표시
                    color = [int(c) for c in random.choice(range(256), size=3)]
                    cv2.rectangle(current_frame, (x1, y1), (x2, y2), color, 2)
                    cv2.putText(current_frame, f'{label} {conf:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

            # 프레임 표시
            cv2.imshow('frame', current_frame)
        
        time.sleep(detection_interval)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            stop_event.set()
            break

# 스레드 생성
receiver_thread = threading.Thread(target=stream_receiver)
detection_thread = threading.Thread(target=object_detection)

# 스레드 시작
receiver_thread.start()
detection_thread.start()

# 메인 스레드에서 키 입력 대기
while not stop_event.is_set():
    if cv2.waitKey(1) & 0xFF == ord('q'):
        stop_event.set()

# 스레드 종료 대기
receiver_thread.join()
detection_thread.join()

urlopen('http://' + ip + "/action?go=stop")
cv2.destroyAllWindows()
