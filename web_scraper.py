# web_scraper.py
# Created August 11 2025 - George Ji

import asyncio

import datetime
import python_weather

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

# import requests
# from bs4 import BeautifulSoup

TOTAL_CAPACITY = 1000

def fetch_timestamp() -> str:
    """Fetch the current timestamp."""
    return datetime.datetime.now().strftime('%m-%d %H:%M')

async def fetch_weather(location: str = 'Storrs CT') -> str:
    """Fetch the current weather for a given location."""
    async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
        weather = await client.get(location)
    return weather.description, weather.feels_like, weather.temperature
    

def fetch_occupancy() -> int:
    """Fetch the current occupancy of UConn Rec."""
    url = 'https://app.safespace.io/api/display/live-occupancy/86fb9e11'
    
    # this method doesn't work because the content is loaded dynamically.
    # response = requests.get(url)
    # soup = BeautifulSoup(response.text, 'html.parser')
    # occupants = soup.select('span')[1].text
    # print(occupants)
    
    # instead, we can use selenium to get the data.
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.get(url)

    # wait for the element to be present
    try:
        occupants_elem = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'occupants'))
        )
        occupants = occupants_elem.text
        return occupants, f'{int(occupants) / TOTAL_CAPACITY * 100}%'
    finally:
        driver.quit()

if __name__ == "__main__":
    timestamp = fetch_timestamp()
    weather = asyncio.run(fetch_weather())
    occupancy = fetch_occupancy()

    print(f"Timestamp: {timestamp}")
    print(f"Weather: {weather}")
    print(f"UConn Rec Occupancy: {occupancy}")