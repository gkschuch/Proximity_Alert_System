#include <Arduino.h>
#include <Ultrasonic.h>

Ultrasonic ultrsonicSensor(11, 10);

void setup()
{
  Serial.begin(9600);
}

void loop()
{
  int distance = ultrsonicSensor.read();

  Serial.print("Distance in CM: ");
  Serial.println(distance);
  delay(1000);
}
