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
  //직진
  Serial.println("go");
  //오른쪽모터
  digitalWrite(IN_11,HIGH);
  analogWrite(IN_12,255);
  
  //왼쪽모터
  digitalWrite(IN_21,LOW);
  analogWrite(IN_22,255);
  delay(2000);
  

  //후진
  Serial.println("back");
  //오른쪽모터
  digitalWrite(IN_11,LOW);
  analogWrite(IN_12,255);
  
  //왼쪽모터
  digitalWrite(IN_21,HIGH);
  analogWrite(IN_22,255);
  delay(2000);


  //왼쪽이동
  Serial.println("left");
  //오른쪽모터
  digitalWrite(IN_11,HIGH);
  analogWrite(IN_12,255);
  
  //왼쪽모터
  digitalWrite(IN_21,HIGH);
  analogWrite(IN_22,0);
  delay(2000);


  //오른쪽이동
  Serial.println("right");
  //오른쪽모터
  digitalWrite(IN_11,LOW);
  analogWrite(IN_12,0);
  
  //왼쪽모터
  digitalWrite(IN_21,LOW);
  analogWrite(IN_22,255);
  delay(2000);
}
