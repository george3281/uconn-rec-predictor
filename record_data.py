# record_data.py
# Created August 11 2025 - George Ji

import csv
import os
import time
import datetime
import web_scraper

def record_data(filename: str = 'rec_data.csv'):
    """Record data fetched from web_scraper to a CSV file."""
    start = time.time()
    data = web_scraper.fetch_data()
    
    # Check if file exists to determine if we need to write headers
    file_exists = os.path.exists(filename)
    
    # Open file in append mode
    with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['timestamp', 'hour', 'day_of_week', 'day_of_year', 'semester_progress', 'weather', 'temperature', 'occupancy']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write header only if file is new
        if not file_exists:
            writer.writeheader()
        
        # Write the data row
        writer.writerow(data)
    end = time.time()

    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    print(f"{timestamp}: data recorded to {filename} in {end - start:.2f} seconds.")

def automate_recording(interval: int = 1200, filename: str = 'rec_data.csv'):
    """Automate data recording at specified intervals (in seconds)."""
    print(f"Starting data recording every {interval} seconds. Press Ctrl+C to stop.")
    try:
        while True:
            record_data(filename)
            time.sleep(interval)
    except KeyboardInterrupt:
        print("Data recording stopped by user.")


if __name__ == "__main__":
    automate_recording()

