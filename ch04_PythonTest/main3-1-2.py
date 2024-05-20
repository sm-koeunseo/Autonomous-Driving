import cv2
import numpy as np
from urllib.request import urlopen
import time

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
            
            cv2.imshow("AI CAR Streaming", img)
            
            key = cv2.waitKey(1)
            if key == ord('q'):
                break

    except:
        print("에러")
        pass

cv2.destroyAllWindows()

# main3-1-2.py
# 영상스트리밍 데이터 OpenCV를 이용하여 영상출력