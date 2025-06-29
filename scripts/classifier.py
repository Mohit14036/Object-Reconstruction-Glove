import numpy as np
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.ensemble import RandomForestClassifier

file_path = "../data/classificationTraining.csv"  
df = pd.read_csv(file_path)
print(1)
X = df[["Flex1", "Flex2", "Flex3", "Flex4","Flex5"]].values

y=df["Label"].values
print(y)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(1)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
print(1)

model = RandomForestClassifier(n_estimators=100,max_depth=10,random_state=42)
model.fit(X_train_scaled, y_train)
print(1)
y_pred = model.predict(X_test_scaled)
accuracy=accuracy_score(y_test,y_pred)
print("Accuracy" ,accuracy)
print(classification_report(y_test,y_pred))
joblib.dump(model, "../models/shapeClassifier.pkl")
joblib.dump(scaler, "../models/classificationScaler.pkl")
print("Model and scaler saved successfully!")
