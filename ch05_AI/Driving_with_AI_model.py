import cv2
import numpy as np
from urllib.request import urlopen
from keras.models import load_model
import numpy as np
import threading
import time

#모델불러오기
model = load_model(r"./converted_keras/keras_model.h5", compile=False)
class_names = open(r"./converted_keras/labels.txt", "r").readlines()

# IP를 수정하여 진행하세요.
ip = '192.168.137.237'
stream = urlopen('http://' + ip + ':81/stream')
buffer = b''
# 차량의 속도는 80으로 세팅되어 있으나, 변경하면서 진행하셔도 됩니다.
urlopen('http://' + ip + "/action?go=speed80")

image_flag = 0
def image_process_thread():
    global img
    global image_flag
    while True:
        if image_flag == 1:
            img = np.asarray(img, dtype=np.float32).reshape(1, 224, 224, 3)
            img = (img / 127.5) - 1

            # AI모델을 활용한 예측
            prediction = model.predict(img)
            index = np.argmax(prediction)
            class_name = class_names[index]
            confidence_score = prediction[0][index]
            percent = int(str(np.round(confidence_score * 100))[:-2])

            # AI 예측 정확도가 80%이상일때만 조작 변경
            if "go" in class_name[2:] and percent >= 80:
                print("직진:",str(np.round(confidence_score * 100))[:-2],"%")
                urlopen('http://' + ip + "/action?go=forward")
            elif "left" in class_name[2:] and percent >= 80:
                print("왼쪽:",str(np.round(confidence_score * 100))[:-2],"%")
                urlopen('http://' + ip + "/action?go=left")
            elif "right" in class_name[2:] and percent >= 80:
                print("오른쪽:",str(np.round(confidence_score * 100))[:-2],"%")
                urlopen('http://' + ip + "/action?go=right")

            image_flag = 0
            
# 데몬 스레드를 생성합니다.
daemon_thread = threading.Thread(target=image_process_thread)
daemon_thread.daemon = True 
daemon_thread.start()

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
            img = img[height // 2:height-30, :]

            # 크기 조절
            img = cv2.resize(img, (224, 224), interpolation=cv2.INTER_AREA)

            cv2.imshow("AI CAR Streaming", img)
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