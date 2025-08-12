# config.py
# Created August 11 2025 - George Ji

URL='https://app.safespace.io/api/display/live-occupancy/86fb9e11?view=percent'
SEMESTERS={
    'summer_2025': {'start': '2025-05-20', 'end': '2025-08-15'},
    'fall_2025': {'start': '2025-08-25', 'end': '2025-12-15'},
    'spring_2026': {'start': '2026-01-20', 'end': '2026-05-10'},
    # add more semesters as needed
}
WEATHER={
    'Sunny': 1,
    'Partly cloudy': 2,
    'Cloudy': 3,
    'Rain': 4,
    'Thunderstorm': 5,
    'Snow': 6,
    'Fog': 7,
    'Clear': 8   
}
DATASET = 'data/rec_data.csv'