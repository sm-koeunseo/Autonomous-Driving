import cv2
import numpy as np
from urllib.request import urlopen

ip = '192.168.137.20'
stream = urlopen('http://' + ip + ':81/stream')
buffer = b''

while True:
    buffer += stream.read(4096)
    print(buffer)

# main3-1-1.py
# 자율주행 자동차 영상스트리밍 데이터확인