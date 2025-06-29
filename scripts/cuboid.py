import numpy as np
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.ensemble import RandomForestRegressor
file_path = "../data/cuboidTraining.csv" 
df = pd.read_csv(file_path)
print(1)
X = df[["Flex2", "Flex3", "Flex4","Flex5"]].values
y=df["Label"].values

print(y)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(1)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
print(X_train_scaled)
X_test_scaled = scaler.transform(X_test)
print(1)

model=RandomForestRegressor(n_estimators=100)
model.fit(X_train_scaled, y_train)
print(1)
y_pred = model.predict(X_test_scaled)
print(f"Mean Absolute Error: {mean_absolute_error(y_test, y_pred):.2f}")
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f"Mean Squared Error (MSE): {mse:.2f}")
print(f"R-squared (R² Score): {r2:.2f}")

joblib.dump(model, "../models/sideLength.pkl")
joblib.dump(scaler, "../models/cuboidScaler.pkl")
print("Model and scaler saved successfully!")
