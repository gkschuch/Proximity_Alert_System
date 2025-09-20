import time
import serial
from PySide6.QtCore import QObject, Signal, Slot
from config import SERIAL_PORT, BAUD_RATE

class Worker(QObject):
    distance_updated = Signal(int)

    def __init__(self):
        super().__init__()
        self.arduino = None
        self._is_running = True

    @Slot()
    def run(self):

        self.arduino = serial.Serial(port=SERIAL_PORT, baudrate=BAUD_RATE, timeout=2)
        time.sleep(2)
        self.arduino.reset_input_buffer()


        while self._is_running:
            self.arduino.write(b'D')
            line = self.arduino.readline().decode('utf-8').strip()
            if line:
                distance = int(line)
                self.distance_updated.emit(distance)
            time.sleep(0.2)
        
        if self.arduino and self.arduino.is_open:
            self.arduino.close()

    
    def stop(self):
        self._is_running = False