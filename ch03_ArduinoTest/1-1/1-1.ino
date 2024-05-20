#define LED_BUILTIN 4

void setup() {
  Serial.begin(9600);
  pinMode(LED_BUILTIN,OUTPUT);
}

void loop() {
  digitalWrite(LED_BUILTIN,HIGH);
  delay(2000);
  digitalWrite(LED_BUILTIN,LOW);
  delay(2000);
}

//8-1-#
//hint : 조명의 밝기가 어떻게 변화하는지 관찰