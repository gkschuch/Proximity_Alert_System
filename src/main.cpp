#include <Arduino.h>
#include <Ultrasonic.h>
#include "config.h"

Ultrasonic ultrasonicSensor(TRIGGER_PIN, ECHO_PIN);

void sendDistance(int distance)
{
  Serial.println(distance);
}

void setLedState(int distance)
{
  digitalWrite(RED_LED_PIN, LOW);
  digitalWrite(YELLOW_LED_PIN, LOW);
  digitalWrite(GREEN_LED_PIN, LOW);

  if (distance <= DANGER_THRESHOLD)
  {
    digitalWrite(RED_LED_PIN, HIGH);
  }
  else if (distance <= WARNING_THRESHOLD)
  {
    digitalWrite(YELLOW_LED_PIN, HIGH);
  }
  else
  {
    digitalWrite(GREEN_LED_PIN, HIGH);
  }
}

void setup()
{
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(YELLOW_LED_PIN, OUTPUT);
  pinMode(GREEN_LED_PIN, OUTPUT);
}

void loop()
{
  int distance = ultrasonicSensor.read();
  if (Serial.available() > 0)
  {
    char command = Serial.read();

    if (command == 'D')
    {
      sendDistance(distance);
    }
  }
  setLedState(distance);
}