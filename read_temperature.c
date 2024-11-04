#include "DS18B20.h"
#include <LiquidCrystal_I2C.h>

#define ONE_WIRE_BUS 0

OneWire oneWire(ONE_WIRE_BUS);
DS18B20 sensor(&oneWire);

int lcdColumns = 16;
int lcdRows = 2;
LiquidCrystal_I2C lcd(0x27, lcdColumns, lcdRows);  


void setup(void)
{
  Serial.begin(9600);

  sensor.begin();

  lcd.init();
  lcd.backlight();
}


void loop(void)
{
  sensor.requestTemperatures();
  lcd.setCursor(0,0);
  char str[5];
  sprintf(str, "%.2f", sensor.getTempC());
  hello(str);
}

void hello(char msg[]){
  lcd.print(msg);
  delay(1000);
  lcd.clear();
  delay(500);
}
