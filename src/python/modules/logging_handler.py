import csv
from datetime import datetime
from config import LOG_FILE

def log_danger_event(distance):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = [timestamp, distance]

    with open(LOG_FILE, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(log_entry)