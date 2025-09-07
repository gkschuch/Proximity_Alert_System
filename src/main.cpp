#include <Arduino.h>
#include <Ultrasonic.h>
#include "config.h"

Ultrasonic ultrasonicSensor(TRIGGER_PIN, ECHO_PIN);

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
  checkSerialCommands();

  sendDistance();
  delay(50);
}

/**
 * @brief Checks for commands received via the serial port to control the LEDs.
 *
 * This function reads a line from the serial buffer, removes whitespace,
 * and compares the command to the strings "RED", "YELLOW", or "GREEN". It then
 * turns on the corresponding LED and turns off the other two.
 */
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

/**
 * @brief Measures the distance with the sensor and sends it via the serial port.
 *
 * This function uses the `read()` method from the Ultrasonic library to get the
 * distance in centimeters and prints it to the serial port for Python to read.
 */
void sendDistance()
{
  int distance = ultrasonicSensor.read();

  Serial.println(distance);
}