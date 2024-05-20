#define LED_BUILTIN 4

void setup() {
  Serial.begin(9600);
}

void loop() {
  if(Serial.available() > 0 )
  {
    char sData = Serial.read();
    if(sData == 'a') analogWrite(LED_BUILTIN,0);
    else if(sData == 'b') analogWrite(LED_BUILTIN,127);
    else if(sData == 'c') analogWrite(LED_BUILTIN,255);
  }
}
