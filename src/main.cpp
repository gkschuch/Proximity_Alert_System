#include <Arduino.h>
#include <Ultrasonic.h>
#include "config.h"

Ultrasonic ultrsonicSensor(TRIGGER_PIN, ECHO_PIN);

void checkSerialCommands();
void sendDistance();

void setup()
{
  Serial.begin(9600);
  pinMode(RED_LED_PIN, OUTPUT);
  pinMode(YELLOW_LED_PIN, OUTPUT);
  pinMode(GREEN_LED_PIN, OUTPUT);
}

void loop()
{
  digitalWrite(GREEN_LED_PIN, LOW);
  digitalWrite(RED_LED_PIN, LOW);
  digitalWrite(YELLOW_LED_PIN, LOW);

  checkSerialCommands();

  sendDistance();
}

void checkSerialCommands()
{
  if (Serial.available() > 0)
  {
    String command = Serial.readStringUntil('\n');
    command.trim();
    if (command == "RED")
    {
      digitalWrite(GREEN_LED_PIN, LOW);
      digitalWrite(RED_LED_PIN, HIGH);
      digitalWrite(YELLOW_LED_PIN, LOW);
    }
    else if (command == "YELLOW")
    {
      digitalWrite(GREEN_LED_PIN, LOW);
      digitalWrite(RED_LED_PIN, LOW);
      digitalWrite(YELLOW_LED_PIN, HIGH);
    }
    else if (command == "GREEN")
    {
      digitalWrite(GREEN_LED_PIN, HIGH);
      digitalWrite(RED_LED_PIN, LOW);
      digitalWrite(YELLOW_LED_PIN, LOW);
    }
  }
}
void sendDistance()
{
  int distance = ultrsonicSensor.read();
  Serial.println(distance);
}