"""
main.py
-------
FastAPI backend for the House Price Prediction project.

Run with:
    uvicorn main:app --reload --port 8000
"""

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from schema import HouseFeatures, PredictionResponse

app = FastAPI(title="House Price Prediction API", version="1.0")

# Allow Streamlit (running on a different port) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

import os
MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "model_linear.pkl")


@app.get("/")
def root():
    return {"message": "House Price Prediction API is running"}


@app.post("/predict", response_model=PredictionResponse)
def predict(features: HouseFeatures):
    try:
        model = joblib.load(MODEL_PATH)
    except FileNotFoundError:
        raise HTTPException(
            status_code=500,
            detail="Model not found. Run train.py first to train and save the model.",
        )

    input_df = pd.DataFrame([features.dict()])
    predicted_price = model.predict(input_df)[0]

    return PredictionResponse(predicted_price_lakhs=round(float(predicted_price), 2))
