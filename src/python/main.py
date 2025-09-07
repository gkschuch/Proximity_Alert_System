import serial
import time
SERIAL_PORT = 'COM3'
BAUD_RATE = 9600

def main():
    print('Initializing connection...')
    try:
        arduino=serial.Serial(port =SERIAL_PORT, baudrate=BAUD_RATE)
        time.sleep(2)
        print('Connection established')
        while True:
            line = arduino.readline().decode('utf-8').strip()
            if line:
                try:
                    distance = int(line)
                    if distance < 5:
                        print("RED ZONE!!! Danger")
                        arduino.write(b'RED\n')
                    elif distance < 10:
                        print('YELLOW ZONE! Object Close')
                        arduino.write(b'YELLOW\n')
                    else:
                        print(f"Safe distance: {distance} cm. GREEN ZONE")
                        arduino.write(b'GREEN\n')
                except ValueError:
                    print('Data received is not a INT')
        
            time.sleep(0.1)
    except serial.SerialException as e:
        print(f"ERROR: Unable to connect to port {SERIAL_PORT}.")
        print(f"DETAILS: {e}")
        print("Check the serial port and whether the Arduino is connected.")



if __name__ == '__main__':
    main()