import cv2
import numpy as np
from urllib.request import urlopen
import os
import re

os.chdir(os.path.dirname(os.path.abspath(__file__)))

ip = '192.168.137.91'
stream = urlopen('http://' + ip + ':81/stream')
buffer = b''
urlopen('http://' + ip + "/action?go=speed40")

if not os.path.isdir('images'):
    os.mkdir("images")

existing_images = [f for f in os.listdir('images') if re.match(r'image_\d+\.png', f)]
if existing_images:
    existing_numbers = [int(re.findall(r'\d+', f)[0]) for f in existing_images]
    image_cnt = max(existing_numbers) + 1
else:
    image_cnt = 0

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
            elif key == ord('s'):
                print("이미지 저장:", image_cnt)
                cv2.imwrite(f'images/image_{image_cnt}.png', img)
                image_cnt += 1

    except Exception as e:
        print("에러:", str(e))
        pass

urlopen('http://' + ip + "/action?go=stop")
cv2.destroyAllWindows()
