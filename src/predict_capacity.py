# predict_capacity.py
# Created August 11 2025 - George Ji

import joblib
import asyncio
import web_scraper as wb

def predict_occupancy(hour, day_of_week, semester_progress, weather, temperature):
   # If outside operating hours, return 0 occupancy.
   isweekend = day_of_week in (5, 6)  # Saturday or Sunday
   if isweekend and (int(hour) < 10 or int(hour) > 18):
    return 0.0
   if not isweekend and (int(hour) < 6 or int(hour) > 22):
    return 0.0
   
   # Load saved components
   model = joblib.load('models/model.pkl')
   scaler = joblib.load('models/scaler.pkl')
   selector = joblib.load('models/selector.pkl')
   
   # Prepare input (all 5 features)
   data = [[hour, day_of_week, semester_progress, weather, temperature]]
   
   # Apply same preprocessing
   scaled = scaler.transform(data)
   selected = selector.transform(scaled)
   
   # Predict
   prediction = model.predict(selected)[0]
   return prediction

if __name__ == "__main__":
    custom_input = input("Press c to enter custom input, or any other key to use current data: ")
    if custom_input.lower() == 'c':
        hour = int(input("Enter hour (0-23): "))
        day_of_week = int(input("Enter day of week (0=Mon, 6=Sun): "))
        semester_progress = float(input("Enter semester progress (0.0-1.0): "))
        weather = int(input("Enter weather code (1-8): "))
        temperature = float(input("Enter temperature (F): "))
        occupancy = predict_occupancy(hour, day_of_week, semester_progress, weather, temperature)
        print(f"Predicted occupancy: {occupancy:.1%}")
    
    else:
        occupancy = predict_occupancy(
        wb.fetch_timestamp()[1],
        wb.fetch_timestamp()[2],
        wb.get_semester_progress(),
        asyncio.run(wb.fetch_weather())[0],
        asyncio.run(wb.fetch_weather())[1],
        )
        print(f"Predicted: {occupancy:.1%} \nActual: {float(wb.fetch_occupancy()):.1%}%")