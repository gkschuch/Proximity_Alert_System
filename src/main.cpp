#include <Arduino.h>
#include <Ultrasonic.h>
#include "config.h"

Ultrasonic ultrasonicSensor(TRIGGER_PIN, ECHO_PIN);

/**
 * @brief Measures the distance and sends the value over serial.
 */
void sendDistance()
{
  int distance = ultrasonicSensor.read();
  Serial.println(distance);
}

/**
 * @brief Sets the state of the LEDs based on a color command.
 * Turns one LED on and the others off.
 * @param colorCommand A character representing the color ('R', 'Y', or 'G').
 */
void setLedState(char colorCommand)
{
  // First, turn all LEDs off to ensure only one is active at a time.
  digitalWrite(RED_LED_PIN, LOW);
  digitalWrite(YELLOW_LED_PIN, LOW);
  digitalWrite(GREEN_LED_PIN, LOW);

  // Now, turn on the correct LED based on the command.
  if (colorCommand == 'R')
  {
    digitalWrite(RED_LED_PIN, HIGH);
  }
  else if (colorCommand == 'Y')
  {
    digitalWrite(YELLOW_LED_PIN, HIGH);
  }
  else if (colorCommand == 'G')
  {
    digitalWrite(GREEN_LED_PIN, HIGH);
  }
}

void setup()
{
  Serial.begin(9600);
  pinMode(RED_LED_PIN, OUTPUT);
  pinMode(YELLOW_LED_PIN, OUTPUT);
  pinMode(GREEN_LED_PIN, OUTPUT);
}

void loop()
{
  // Wait for a command to arrive from Python.
  if (Serial.available() > 0)
  {
    char command = Serial.read();

    if (command == 'D') // 'D' for Distance
    {
      sendDistance();
    }
    else if (command == 'R' || command == 'Y' || command == 'G') // Color Commands
    {
      setLedState(command);
    }
  }
}