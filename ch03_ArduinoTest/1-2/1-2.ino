#define LED_BUILTIN 4

void setup() {
  Serial.begin(9600);
  pinMode(LED_BUILTIN,OUTPUT);
}

void loop() {
  analogWrite(LED_BUILTIN,0);
  delay(1000);
  analogWrite(LED_BUILTIN,50);
  delay(1000);
  analogWrite(LED_BUILTIN,100);
  delay(1000);
  analogWrite(LED_BUILTIN,150);
  delay(1000);
  analogWrite(LED_BUILTIN,200);
  delay(1000);
  analogWrite(LED_BUILTIN,255);
  delay(1000);
}
