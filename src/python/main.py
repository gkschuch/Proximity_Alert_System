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
                if line == 'ALERT':
                    print("Object too close")
        
            time.sleep(0.1)
    except serial.SerialException as e:
        print(f"ERROR: Unable to connect to port {SERIAL_PORT}.")
        print(f"DETAILS: {e}")
        print("Check the serial port and whether the Arduino is connected.")



if __name__ == '__main__':
    main()