import cv2
import numpy as np
from urllib.request import urlopen

ip = '192.168.137.20'
stream = urlopen('http://' + ip + ':81/stream')
buffer = b''

while True:
    buffer += stream.read(4096)
    head = buffer.find(b'\xff\xd8')
    end = buffer.find(b'\xff\xd9')
    
    try:
        if head > -1 and end > -1:
            jpg = buffer[head:end+2]
            buffer = buffer[end+2:]
            img = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_UNCHANGED)

            # 아래부분의 반만 자르기
            height, width, _ = img.shape
            img = img[height // 2:, :]

            # 크기 조절
            img = cv2.resize(img, (224, 224), interpolation=cv2.INTER_AREA)

            cv2.imshow("AI CAR Streaming", img)

            key = cv2.waitKey(1)
            if key == ord('q'):
                break
            elif key == ord('w'):
                print('전진')
            elif key == ord('a'):
                print('왼쪽')
            elif key == ord('d'):
                print('오른쪽')
            elif key == ord('s'):
                print('후진')
            elif key == ord('A'):
                print('왼쪽 회전')
            elif key == ord('D'):
                print('오른쪽 회전')
            elif key == 32: #스페이스바
                print('멈춤')
            elif key == ord('1'):
                print('40%속도')
            elif key == ord('2'):
                print('50%속도')
            elif key == ord('3'):
                print('60%속도')
            elif key == ord('4'):
                print('80%속도')
            elif key == ord('5'):
                print('100%속도')
            
    except:
        print("에러")
        pass

cv2.destroyAllWindows()

# main3-2-2.py
# 키보드 값에 따른 조건문 추가
