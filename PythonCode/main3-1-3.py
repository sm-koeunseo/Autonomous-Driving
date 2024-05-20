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

            cv2.imshow("AI CAR Streaming", img)
            
            key = cv2.waitKey(1)
            if key == ord('q'):
                break

    except:
        print("에러")
        pass

cv2.destroyAllWindows()

# main3-1-3.py
# 이미지의 아래부분 1/2만 잘라 출력하기
