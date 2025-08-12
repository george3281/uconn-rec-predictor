# train_model.py
# Created August 11 2025 - George Ji

import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.feature_selection import SelectKBest, f_regression
from config import DATASET

def train_model(filename: str = DATASET):
    """Train a linear regression model on rec_data.csv"""
    try:
        df = pd.read_csv(filename)
    except FileNotFoundError:
        print(f"Error: {filename} not found")
        return None
    
    df.fillna(df.mean(), inplace=True) # Handle missing values by filling with mean

    target = df['occupancy']
    inputs = df[['hour', 'day_of_week', 'semester_progress', 'weather', 'temperature']]

    print(df.info())  # Check column types and missing values
    print(df.describe())  # Get summary statistics

    # Standardize the features
    scaler = StandardScaler()
    inputs_scaled = scaler.fit_transform(inputs)
    
    # Select features
    selector = SelectKBest(f_regression, k=3)
    inputs_selected = selector.fit_transform(inputs_scaled, target)

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(inputs_selected, target, test_size=0.2, random_state=42)
    
    # Train the model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Make predictions
    y_pred = model.predict(X_test)

    # Evaluate the model
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    # Show selected features
    feature_names = ['hour', 'day_of_week', 'semester_progress', 'weather', 'temperature']
    selected_features = [feature_names[i] for i in selector.get_support(indices=True)]
    print(f"Selected features: {selected_features}")

    print(f"MSE: {mse:.4f}") # Mean Squared Error is the average of the squares of the errors.
    print(f"R² Score: {r2:.4f}") # R² score is the coefficient of determination.

    return model, scaler, selector

if __name__ == "__main__":
    model, scaler, selector = train_model()
    # Save models
    joblib.dump(model, 'models/model.pkl')
    joblib.dump(scaler, 'models/scaler.pkl') 
    joblib.dump(selector, 'models/selector.pkl')