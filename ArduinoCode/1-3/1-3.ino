#define LED_BUILTIN 4

int value = 0;

void setup() {
  Serial.begin(9600);
  pinMode(LED_BUILTIN,OUTPUT);
}

void loop() {
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