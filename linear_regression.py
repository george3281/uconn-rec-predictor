# linear_regression.py
# Created August 11 2025 - George Ji

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression

# potential multicollinearity with day_of_year and semester_progress, but keeping for now
# check correlation matrix before training : df.corr()

if __name__ == "__main__":
    df = pd.read_csv('rec_data.csv')
    df.fillna(df.mean(), inplace=True) # Handle missing values by filling with mean

    target = df['occupancy']
    inputs = df[['hour', 'day_of_week', 'day_of_year', 'semester_progress', 'weather', 'temperature']]

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(target, inputs, test_size=0.2, random_state=42)

    print(df.info())  # Check column types and missing values
    print(df.describe())  # Get summary statistics

    # Standardize the features
    scaler = StandardScaler()
    inputs_scaled = scaler.fit_transform(inputs)

    model = LinearRegression()
    model.fit(X_train, y_train)