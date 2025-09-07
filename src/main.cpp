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

  if (distance < 5)
  {
    Serial.println("ALERT");
  }

  delay(1000);
}
