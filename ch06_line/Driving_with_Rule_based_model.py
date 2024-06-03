import cv2
import numpy as np
from urllib.request import urlopen
import threading



# ip 변경 필요
ip = '192.168.137.202'
stream = urlopen('http://' + ip + ':81/stream')
buffer = b''
urlopen('http://' + ip + "/action?go=speed100") # 차량 속도 변경

image_flag = 0

def image_process_thread():
    global image_flag, car_state
    while True:
        if image_flag == 1:
            if car_state == "go":
                urlopen('http://' + ip + "/action?go=forward")
            elif car_state == "right":
                urlopen('http://' + ip + "/action?go=right")
            elif car_state == "left":
                urlopen('http://' + ip + "/action?go=left")
            image_flag = 0
            
# 데몬 스레드를 생성 -> 이미지 프로세싱을 별도 스레드에서 진행
daemon_thread = threading.Thread(target=image_process_thread)
daemon_thread.daemon = True 
daemon_thread.start()

car_state = "go"
left = 30
right = 10
while True:
    buffer += stream.read(4096)
    head = buffer.find(b'\xff\xd8')
    end = buffer.find(b'\xff\xd9')
    
    try:
        if head > -1 and end > -1:
            jpg = buffer[head:end+2]
            buffer = buffer[end+2:]
            img = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
            
            # 이미지 전처리 1: 이미지 크기 조절 (세로, 가로)
            height, width, _ = img.shape
            img = img[height // 2:height-20, :-20] # 더 자르고 싶으면 -15
            
            # 색상 필터링으로 검정색 선 추출
            lower_bound = np.array([0, 0, 0])
            upper_bound = np.array([255, 255, 80])
            mask = cv2.inRange(img, lower_bound, upper_bound)
            cv2.imshow("mask", mask)
            
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
            cv2.circle(img, (cX, cY), 10, (0, 255, 0), -1)
            
            # 경계값 시각화 (점선으로 표시)
            left_boundary = width // 2 - left  # 왼쪽 경계
            right_boundary = width // 2 + right  # 오른쪽 경계
            cv2.line(img, (width // 2, 0), (width // 2, height), (0, 255, 0), 1, lineType=cv2.LINE_AA, shift=0)
            cv2.line(img, (left_boundary, 0), (left_boundary, height), (255, 0, 0), 1, lineType=cv2.LINE_AA, shift=0)
            cv2.line(img, (right_boundary, 0), (right_boundary, height), (255, 0, 0), 1, lineType=cv2.LINE_AA, shift=0)
            
            cv2.imshow("AI CAR Streaming", img)

            # 무게중심 기준으로 판단기준 변경
            if center_offset  < -right:
                print("오른쪽")
                car_state = "right"
            elif center_offset  > left:
                print("왼쪽")
                car_state = "left"
            else:
                print("직진")
                car_state = "go"

            image_flag = 1
            key = cv2.waitKey(1)
            if key == ord('q'):
                urlopen('http://' + ip + "/action?go=stop")
                break

    except:
        print("에러")
        pass

urlopen('http://' + ip + "/action?go=stop")
cv2.destroyAllWindows()