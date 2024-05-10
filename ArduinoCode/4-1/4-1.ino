#include <Wire.h>               
#include "SSD1306Wire.h"     

SSD1306Wire display(0x3c, 0, 2, GEOMETRY_128_32);

void setup() {
  Serial.begin(115200);
  Serial.println();
  Serial.println();

  display.init();

  display.flipScreenVertically();
  display.setFont(ArialMT_Plain_10);

}


void loop() {
  display.clear();
  display.setFont(ArialMT_Plain_10);
  display.setTextAlignment(TEXT_ALIGN_LEFT);
  display.drawString(0, 10, "HELLO");
  display.display();
  delay(2000);
  
  display.clear();
  display.setFont(ArialMT_Plain_10);
  display.setTextAlignment(TEXT_ALIGN_LEFT);
  display.drawString(0, 10, "AI CAR");
  display.display();
  delay(2000);
}
