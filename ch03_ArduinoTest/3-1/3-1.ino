#define IN_11 12
#define IN_12 13
#define IN_21 15
#define IN_22 14

void setup() {
  Serial.begin(9600);
  pinMode(IN_11,OUTPUT);
  pinMode(IN_12,OUTPUT);
  pinMode(IN_21,OUTPUT);
  pinMode(IN_22,OUTPUT);
}

void loop() {
  Serial.println("go");
  //오른쪽모터
  digitalWrite(IN_11,HIGH);
  analogWrite(IN_12,127);
  
  //왼쪽모터
  digitalWrite(IN_21,LOW);
  analogWrite(IN_22,127);
  delay(2000);
}

//땅에 놓고 작동하세요(책상에서 낙하 주의).