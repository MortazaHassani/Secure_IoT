#include <Arduino.h>
#include "DHT.h"

#define DHTPIN 26     // Digital pin connected to the DHT sensor
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

int wLED = 33;
int rLED = 32;
int pButton1 = 27;

void setup() {
  // put your setup code here, to run once:
Serial.begin(115200);

  dht.begin();

pinMode(rLED,OUTPUT);
pinMode(wLED, OUTPUT);
pinMode(pButton1, INPUT);


}

void loop() {
  // put your main code here, to run repeatedly:

//// Blink LED
// digitalWrite(rLED,HIGH);
// digitalWrite(wLED,LOW);
// delay(1000);
// digitalWrite(rLED,LOW);
// digitalWrite(wLED,HIGH);
// Serial.println("ESP32");
// delay(1000);

////Push button turn on Red
digitalWrite(rLED,LOW);
if (digitalRead(pButton1)==1){
  digitalWrite(rLED,HIGH);
}


//// Toggle Mechanism
// int LEDstate= 0;

// if (digitalRead(pButton1)==1 && LEDstate==0){
//   digitalWrite(rLED,HIGH);
//   LEDstate = 1;
// }

//  if(digitalRead(pButton1)==1 && LEDstate==1){
//     digitalWrite(rLED,LOW);
//     LEDstate=0;
//   }

float hmdt = dht.readHumidity();
float tmpr = dht.readTemperature();

if (isnan(hmdt) || isnan(tmpr)) {
    Serial.println(F("Failed to read from DHT sensor!"));
    return;
  }

float hic = dht.computeHeatIndex(tmpr, hmdt, false); // Compute heat index in Celsius (isFahreheit = false)

  Serial.print(F("Humidity: "));
  Serial.print(hmdt);
  Serial.print(F("%  Temperature: "));
  Serial.print(tmpr);
  Serial.print(F("°C "));
  Serial.print(F(" Heat index: "));
  Serial.print(hic);
  Serial.print(F("°C "));
  Serial.println("\n");

}
