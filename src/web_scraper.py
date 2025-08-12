# web_scraper.py
# Created August 11 2025 - George Ji

import asyncio
import datetime
import python_weather
from config import URL, SEMESTERS, WEATHER
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

# import requests
# from bs4 import BeautifulSoup

def fetch_timestamp() -> list[str]:
    """Fetch the current timestamp."""
    return datetime.datetime.now().strftime('%Y-%m-%d_%H:%M %H %w %j').split()

async def fetch_weather(location: str = 'Storrs CT') -> str:
    """Fetch the current weather for a given location."""
    async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
        weather = await client.get(location)
    return [WEATHER.get(weather.description, 0), weather.temperature, weather.description]
    

    
def get_current_semester() -> str:
    """Get the current semester based on the current date."""
    today = datetime.date.today()
    for semester, dates in SEMESTERS.items():
        start = datetime.datetime.strptime(dates['start'], '%Y-%m-%d').date()
        end = datetime.datetime.strptime(dates['end'], '%Y-%m-%d').date()
        if start <= today <= end:
            return semester
    return 0

def get_semester_progress():
    current_semester = get_current_semester()
    if current_semester:
        today = datetime.date.today()
        start = datetime.datetime.strptime(SEMESTERS[current_semester]['start'], '%Y-%m-%d').date()
        end = datetime.datetime.strptime(SEMESTERS[current_semester]['end'], '%Y-%m-%d').date()
        total_days = (end - start).days
        elapsed_days = (today - start).days
        return "%0.2f" % (elapsed_days / total_days)
    return 0

def fetch_occupancy() -> int:
    """Fetch the current occupancy of UConn Rec."""    
    # this method doesn't work because the content is loaded dynamically.
    # response = requests.get(url)
    # soup = BeautifulSoup(response.text, 'html.parser')
    # occupants = soup.select('span')[1].text
    # print(occupants)
    
    # instead, we can use selenium to get the data.
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.get(URL)

    # wait for the element to be present
    try:
        occupants_elem = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.ID, 'occupancyPct'))
        )
        occupants = occupants_elem.text
        return "%0.2f" % (int(occupants.strip('%')) / 100)
    finally:
        driver.quit()

def fetch_data() -> tuple[str, str, int]:
    """Fetch timestamp, weather, and occupancy data."""
    timestamp = fetch_timestamp()
    weather = asyncio.run(fetch_weather())
    occupancy = fetch_occupancy()
    semester_progress = get_semester_progress()
    return {
        'hour': timestamp[1],
        'day_of_week': timestamp[2],
        'semester_progress': semester_progress,
        'weather': weather[0],
        'temperature': weather[1],
        'occupancy': occupancy
    }

if __name__ == "__main__":
    print(fetch_data())