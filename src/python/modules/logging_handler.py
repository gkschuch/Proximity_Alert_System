import csv
from datetime import datetime
from config import LOG_FILE

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