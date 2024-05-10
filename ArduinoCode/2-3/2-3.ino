void setup() {
  Serial.begin(115200);
}

void loop() {
  Serial.println("hello");
  delay(1000);
}

//8-2-3
//mission : 통신속도 변경으로 인한 현상을 관찰하고, 오류 정상화 방안