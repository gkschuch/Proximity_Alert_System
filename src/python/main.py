import serial
import time
import csv
from datetime import datetime

SERIAL_PORT = 'COM3'
BAUD_RATE = 9600

LOG_FILE = 'danger_log.csv'

def log_danger_event(distance):
    """
    Records a new danger zone event to the CSV log file.
    Includes the exact timestamp and the distance that triggered the alert.
    """
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = [timestamp, distance]

    # Open the file in 'append' mode to add a new line.
    # The file is created if it doesn't exist.
    with open(LOG_FILE, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(log_entry)

def main():
    """
    Main function to run the proximity alert system with LED control and logging.
    """
    print("Starting proximity alert system with logging...")
    
    # State variable to track if we are already in the danger zone.
    # This prevents logging the same event multiple times.
    is_in_danger = False

    try:
        # Establish serial connection
        arduino = serial.Serial(port=SERIAL_PORT, baudrate=BAUD_RATE, timeout=2)
        time.sleep(2)
        arduino.reset_input_buffer()
        print("Connection established.")

        while True:
            # 1. REQUEST DISTANCE from Arduino
            arduino.write(b'D')

            # 2. READ THE RESPONSE
            line = arduino.readline().decode('utf-8').strip()

            if line:
                try:
                    distance = int(line)
                    print(f"Distance: {distance} cm")

                    # 3. DECIDE THE COLOR and CHECK FOR LOGGING EVENT
                    color_command = ''
                    if distance < 10:
                        color_command = 'R'  # RED
                        print("--> Danger Zone! Sending RED command.")
                        
                        # If we just entered the danger zone, log it.
                        if not is_in_danger:
                            log_danger_event(distance)
                            is_in_danger = True 
                    
                    elif distance < 30:
                        color_command = 'Y'  # YELLOW
                        print("--> Warning Zone! Sending YELLOW command.")
                        is_in_danger = False 
                    
                    else:
                        color_command = 'G'  # GREEN
                        print("--> Safe Zone! Sending GREEN command.")
                        is_in_danger = False 

                    # 4. SEND THE COLOR COMMAND to Arduino
                    arduino.write(color_command.encode())

                except ValueError:
                    print(f"Received non-numeric data: '{line}'")
            else:
                print("Arduino did not respond to the distance request.")

            # Control the update frequency of the system
            time.sleep(0.2)

    except serial.SerialException as e:
        print(f"ERROR: Could not connect to port {SERIAL_PORT}.")
        print("Please check the port and make sure no other program is using it.")

if __name__ == '__main__':
    main()