import time
import serial
from PySide6.QtCore import QObject, Signal, Slot
from config import SERIAL_PORT, BAUD_RATE

class Worker(QObject):
    """
    Manages serial communication with the Arduino in a background thread.

    Signals:
        distance_updated (Signal): Emits the new distance (int) when received.
    """
    distance_updated = Signal(int)

    def __init__(self):
        super().__init__()
        self.arduino = None
        self._is_running = True

    @Slot()
    def run(self):
        """
        The main loop that communicates with the Arduino.
        This method is executed when the thread starts.
        """
        try:
            self.arduino = serial.Serial(port=SERIAL_PORT, baudrate=BAUD_RATE, timeout=2)
            time.sleep(2)
            self.arduino.reset_input_buffer()
            print("Worker: Arduino connection established.")
        except serial.SerialException as e:
            print(f"Worker Error: Could not connect to Arduino. {e}")
            return # Exit if connection fails

        while self._is_running:
            try:
                self.arduino.write(b'D') # Request a distance reading
                line = self.arduino.readline().decode('utf-8').strip()
                if line:
                    distance = int(line)
                    self.distance_updated.emit(distance) # Emit the new value
                time.sleep(0.2) # Control the update frequency
            except (serial.SerialException, ValueError, OSError) as e:
                print(f"Worker loop error: {e}")
                self._is_running = False # Stop the loop on error
        
        if self.arduino and self.arduino.is_open:
            self.arduino.close()
        print("Worker: Thread has finished.")
    
    def stop(self):
        """Stops the worker's loop."""
        print("Worker: Stop signal received.")
        self._is_running = False