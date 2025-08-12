import joblib
import asyncio
import web_scraper as wb

def predict_occupancy(hour, day_of_week, semester_progress, weather, temperature):
   # TODO: Add logic to handle when Rec is closed.
   
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
    occupancy = predict_occupancy(
        wb.fetch_timestamp()[1],
        wb.fetch_timestamp()[2],
        wb.get_semester_progress(),
        asyncio.run(wb.fetch_weather())[0],
        asyncio.run(wb.fetch_weather())[1],
    )
    print(f"Predicted: {occupancy:.1%}")