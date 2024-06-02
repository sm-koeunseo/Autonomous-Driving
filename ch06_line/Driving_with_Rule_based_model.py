import cv2
import numpy as np
from urllib.request import urlopen
import threading

# 수정사항 1 : IP를 수정하여 진행하세요.
ip = '192.168.137.169'
stream = urlopen('http://' + ip + ':81/stream')
buffer = b''
# 수정사항 2 : 차량의 속도는 80으로 세팅되어 있으나, 변경하면서 진행하셔도 됩니다.
urlopen('http://' + ip + "/action?go=speed80")

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
            
# 데몬 스레드를 생성합니다 (이미지 프로세싱을 별도 스레드에서 진행(원활한 통신을 위해)).
daemon_thread = threading.Thread(target=image_process_thread)
daemon_thread.daemon = True 
daemon_thread.start()

car_state = "go"
while True:
    buffer += stream.read(4096)
    head = buffer.find(b'\xff\xd8')
    end = buffer.find(b'\xff\xd9')
    
    try:
        if head > -1 and end > -1:
            jpg = buffer[head:end+2]
            buffer = buffer[end+2:]
            img = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
            
            #이미지 전처리 1 : 이미지 크기 조절
            height, width, _ = img.shape
# 수정사항 3 : 아래부분 삭제 한 영역(-10)은 변경하셔도 됩니다(카메라 노이즈 제거용)
            img = img[height // 2:height-10, :]
            
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
            cv2.imshow("AI CAR Streaming", img)

# 수정사항 4 : 현재 무게중심 위치가 -10~10은 직진하도록 설계, 이를 변경하여 최적의 성능을 찾아보세요.
            if center_offset < -10:
                print("오른쪽")
                car_state = "right"
            elif center_offset > 10:
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
