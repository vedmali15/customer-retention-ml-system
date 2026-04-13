from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib

# Initialize FastAPI
app = FastAPI()

# Load trained model
model = joblib.load("../models/model.pkl")


# -------- INPUT SCHEMA (VALIDATION) --------
class CustomerData(BaseModel):
    tenure: int
    MonthlyCharges: float
    TotalCharges: float
    Contract: str
    PaymentMethod: str
    SeniorCitizen: int


# -------- PREPROCESSING FUNCTION --------
def preprocess_input(data: CustomerData):
    df = pd.DataFrame([data.dict()])

    # Convert categorical variables using one-hot encoding
    df = pd.get_dummies(df)

    # Align with training features
    model_features = model.feature_names_in_
    df = df.reindex(columns=model_features, fill_value=0)

    return df


# -------- ROOT ENDPOINT --------
@app.get("/")
def home():
    return {"message": "Customer Churn Prediction API is running"}


# -------- PREDICTION ENDPOINT --------
@app.post("/predict")
def predict(data: CustomerData):
    try:
        processed_data = preprocess_input(data)

        prediction = model.predict(processed_data)[0]
        probability = model.predict_proba(processed_data)[0][1]

        return {
            "churn_prediction": int(prediction),
            "churn_probability": float(probability)
        }

    except Exception as e:
        return {"error": str(e)}