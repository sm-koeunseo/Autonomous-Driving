import cv2
import numpy as np
from urllib.request import urlopen
import os
import re

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# IP를 수정하여 진행하세요.
ip = '192.168.137.237'
stream = urlopen('http://' + ip + ':81/stream')
buffer = b''
# 이미지 저장을 위한 주행은 속도 80으로 설정되어 있습니다 (편의에 따라 변경하셔도 됩니다).
urlopen('http://' + ip + "/action?go=speed80")

def get_next_filename(folder):
    files = [f for f in os.listdir(folder) if re.match(r'.*_(\d+).png', f)]
    numbers = [int(re.search(r'_(\d+).png', file).group(1)) for file in files]
    return max(numbers, default=-1) + 1  

# 폴더 생성 및 초기 파일 번호 설정
for folder, state in (('01_go', 'go'), ('02_left', 'left'), ('03_right', 'right')):
    if not os.path.isdir(folder):
        os.mkdir(folder)
    globals()[f'{state}_cnt'] = get_next_filename(folder)

car_state = 'stop'
while True:
    buffer += stream.read(4096)
    head = buffer.find(b'\xff\xd8')
    end = buffer.find(b'\xff\xd9')
    
    try:
        if head > -1 and end > -1:
            jpg = buffer[head:end+2]
            buffer = buffer[end+2:]
            img = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
            img = img[img.shape[0] // 2:img.shape[0]-30, :]
            img = cv2.resize(img, (224, 224), interpolation=cv2.INTER_AREA)
            cv2.imshow("AI CAR Streaming", img)
            key = cv2.waitKey(1)
            
            if key == ord('q'):
                break
            elif key == ord('w'):
                car_state = 'go'
                urlopen('http://' + ip + "/action?go=forward")
            elif key == ord('a'):
                car_state = 'left'
                urlopen('http://' + ip + "/action?go=left")
            elif key == ord('d'):
                car_state = 'right'
                urlopen('http://' + ip + "/action?go=right")
            elif key == 32:  # Space key
                car_state = 'stop'
                urlopen('http://' + ip + "/action?go=stop")

            if car_state != 'stop':
                folder = f'0{1 if car_state == "go" else 2 if car_state == "left" else 3}_{car_state}'
                filename = f'{folder}/{car_state}_{globals()[f"{car_state}_cnt"]}.png'
                cv2.imwrite(filename, img)
                globals()[f'{car_state}_cnt'] += 1

    except Exception as e:
        print("에러:", e)

urlopen('http://' + ip + "/action?go=stop")
cv2.destroyAllWindows()
