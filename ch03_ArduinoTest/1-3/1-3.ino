#define LED_BUILTIN 4

int value = 0;

void setup() {
  Serial.begin(9600);
  pinMode(LED_BUILTIN,OUTPUT);
}

void loop() {
  // map(현재값, 입력최소값, 입력최대값, 출력최소값, 출력최대값)
  // 현재 0~255까지의 숫자를 받아 0~100 범위로 보여움 (ex.255이 들어가면 100)
  // 1-2 예제와 동일한 결과를 내려면 입력과 출력의 범위를 바꿔야 함
  value = map(0,0,255,0,100);
  analogWrite(LED_BUILTIN,value);
  delay(1000);

  value = map(20,0,255,0,100);
  analogWrite(LED_BUILTIN,value);
  delay(1000);

  value = map(40,0,255,0,100);
  analogWrite(LED_BUILTIN,value);
  delay(1000);

  value = map(60,0,255,0,100);
  analogWrite(LED_BUILTIN,value);
  delay(1000);

  value = map(80,0,255,0,100);
  analogWrite(LED_BUILTIN,value);
  delay(1000);

  value = map(100,0,255,0,100);
  analogWrite(LED_BUILTIN,value);
  delay(1000);
}
