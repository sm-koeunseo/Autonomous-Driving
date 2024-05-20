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
  car_go(127);
  delay(2000);
  
  //후진
  Serial.println("back");
  car_back(127);
  delay(2000);

  //왼쪽이동
  Serial.println("left");
  car_go_left(127);
  delay(2000);

  //오른쪽이동
  Serial.println("right");
  car_go_right(127);
  delay(2000);

  //왼쪽회전
  Serial.println("left turn");
  car_turn_left(127);
  delay(2000);

  //오른쪽회전
  Serial.println("right turn");
  car_turn_right(127);
  delay(2000);
}

// 원래는 오른쪽이 LOW, 왼쪽이 HIGH였음 -> 서로 바꿔야 제대로 제대로 동작
void car_go(int speed){
  //오른쪽모터
  digitalWrite(IN_11,HIGH);
  analogWrite(IN_12,speed);
  
  //왼쪽모터
  digitalWrite(IN_21,LOW);
  analogWrite(IN_22,speed);
}

void car_back(int speed){
  //오른쪽모터
  digitalWrite(IN_11,LOW);
  analogWrite(IN_12,speed);
  
  //왼쪽모터
  digitalWrite(IN_21,HIGH);
  analogWrite(IN_22,speed);
}

// 원래 좌회전이 LOW, 우회전이 HIGH였음
// 전진방향으로 회전 메커니즘을 구현하기 위해 좌회전 시 우측 바퀴가 전진하도록 함
void car_go_left(int speed){
  //오른쪽모터
  digitalWrite(IN_11,HIGH);
  analogWrite(IN_12,speed);
  
  //왼쪽모터
  digitalWrite(IN_21,HIGH);
  analogWrite(IN_22,0);
}

void car_go_right(int speed){
  //오른쪽모터
  digitalWrite(IN_11,LOW);
  analogWrite(IN_12,0);
  
  //왼쪽모터
  digitalWrite(IN_21,LOW);
  analogWrite(IN_22,speed);
}


// 좌회전 시 우측 바퀴가 전진, 좌측 바퀴가 후진
void car_turn_left(int speed){
  //오른쪽모터
  digitalWrite(IN_11,HIGH);
  analogWrite(IN_12,speed);
  
  //왼쪽모터
  digitalWrite(IN_21,HIGH);
  analogWrite(IN_22,speed);
}

void car_turn_right(int speed){
  //오른쪽모터
  digitalWrite(IN_11,LOW);
  analogWrite(IN_12,speed);
  
  //왼쪽모터
  digitalWrite(IN_21,LOW);
  analogWrite(IN_22,speed);
}
