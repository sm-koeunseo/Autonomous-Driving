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

    except:
        print("에러")
        pass

cv2.destroyAllWindows()

# main3-1-4.py
# 이미지의 사이즈를 224x224로 조절
