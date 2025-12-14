# record_data.py
# Created August 11 2025 - George Ji

import csv
import os
import time
import datetime
import web_scraper as wb
from config import SAVE_TO

# run: py src/record_data.py

def record_data(filename: str = SAVE_TO):
    """Record data fetched from web_scraper to a CSV file."""
    start = time.time()
    data = wb.fetch_data()
    
    os.makedirs('data', exist_ok=True)
    filepath = os.path.join('data', filename)
    file_exists = os.path.exists(filepath)
    
    # Open file in append mode
    with open(filepath, 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['hour', 'day_of_week', 'semester_progress', 'weather', 'temperature', 'occupancy']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write header only if file is new
        if not file_exists:
            writer.writeheader()
        
        # Write the data row
        writer.writerow(data)
    end = time.time()

    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    print(f"{timestamp}: data recorded to {filename} in {end - start:.2f} seconds.")

def automate_recording(interval: int = 3600, filename: str = 'rec_data.csv'):
    """Automate data recording at specified intervals (in seconds)."""
    print(f"Starting data recording every {interval} seconds. Press Ctrl+C to stop.")
    try:
        while True:
            record_data(filename)
            time.sleep(interval)
    except KeyboardInterrupt:
        print("Data recording stopped by user.")


if __name__ == "__main__":
    r = input("Press r to record data once, or any other key to start automated recording:")
    if r.lower() == 'r':
        record_data()
    else:
        automate_recording()

