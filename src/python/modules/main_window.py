"""
Defines the main graphical user interface (GUI) for the application.

This module contains the MainWindow class, which builds the dashboard window,
manages the worker thread, and updates the UI based on data.
"""

from PySide6.QtWidgets import QMainWindow, QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import QThread, Slot
from PySide6.QtGui import QFont, QCloseEvent

from modules.arduino_worker import Worker
from modules.logging_handler import log_danger_event
from config import DANGER_THRESHOLD, WARNING_THRESHOLD

class MainWindow(QMainWindow):
    """
    The main application window (GUI).
    """
    def __init__(self):
        super().__init__()
        
        # State variable for the logging logic
        self.is_in_danger = False

        self.setWindowTitle("Proximity Dashboard")
        self.setGeometry(150, 150, 300, 200)

        self._setup_ui()

        self.setup_worker_thread()

    def _setup_ui(self):
        """Creates and arranges the widgets in the window."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.title_label = QLabel("Sensor Distance")
        self.title_label.setFont(QFont("Arial", 16))
        
        self.distance_label = QLabel("--- cm")
        self.distance_label.setFont(QFont("Arial", 48, QFont.Bold))
        self.distance_label.setStyleSheet("color: #3498db;") # Blue

        layout.addWidget(self.title_label)
        layout.addWidget(self.distance_label)

    def setup_worker_thread(self):
        """Creates, configures, and starts the background worker thread."""
        self.thread = QThread()
        self.worker = Worker()
        
        self.worker.moveToThread(self.thread)
        
        # Connect signals and slots
        self.thread.started.connect(self.worker.run)
        self.worker.distance_updated.connect(self.update_ui)
        
        self.thread.start()

    def closeEvent(self, event: QCloseEvent):
        """
        Handles the window close event to safely shut down the worker thread.
        """
        print("Closing application...")
        self.worker.stop()
        self.thread.quit()
        self.thread.wait()
        event.accept()

    @Slot(int)
    def update_ui(self, distance: int):
        """
        Slot that receives the distance from the worker and updates the GUI.
        Also contains the logic for logging danger events.

        Args:
            distance (int): The new distance value received from the Arduino.
        """
        self.distance_label.setText(f"{distance} cm")

        # Logic to change color and handle logging
        if distance < DANGER_THRESHOLD:
            self.distance_label.setStyleSheet("color: #e74c3c;") # Red
            # If we just entered the danger zone, log the event
            if not self.is_in_danger:
                log_danger_event(distance)
                self.is_in_danger = True
        elif distance < WARNING_THRESHOLD:
            self.distance_label.setStyleSheet("color: #f1c40f;") # Yellow
            self.is_in_danger = False # Reset state
        else:
            self.distance_label.setStyleSheet("color: #2ecc71;") # Green
            self.is_in_danger = False # Reset state