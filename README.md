# House Price Prediction — Linear Regression

Day 1 of the daily ML project series: FastAPI backend + Streamlit frontend.

## Algorithm
**Linear Regression** — predicts a continuous target (`Price_Lakhs`) from numeric features:
`Area_sqft, Bedrooms, Bathrooms, Age_years, Distance_to_City_km, Parking_Spaces`.

## Dataset
`data/house_prices.csv` — 200 rows with columns:
`Area_sqft, Bedrooms, Bathrooms, Age_years, Distance_to_City_km, Parking_Spaces, Price_Lakhs`

## Model Performance (on the 20% held-out test split)
- MAE: ~6.67 Lakhs
- R² Score: ~0.89

## Project Structure
```
house-price-prediction/
├── data/
│   └── house_prices.csv
├── backend/
│   ├── train.py            # EDA + training script, saves model_linear.pkl
│   ├── main.py              # FastAPI app — /predict endpoint
│   └── schema.py             # Pydantic request/response models
├── frontend/
│   └── app.py                # Streamlit UI
├── requirements.txt
└── README.md
```

## How to Run

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Train the model (from `backend/`):
   ```
   cd backend
   python train.py
   ```
   This does EDA (correlation heatmap, pairplot), trains the Linear Regression model,
   and saves it as `model_linear.pkl`.

3. Start the FastAPI backend (from `backend/`):
   ```
   uvicorn main:app --reload --port 8000
   ```

4. Start the Streamlit frontend (from `frontend/`, in a separate terminal):
   ```
   streamlit run app.py
   ```

5. Open the Streamlit URL shown in the terminal, enter house details, and click
   **Predict Price**.

## Notes
- `/predict` loads `model_linear.pkl` at request time, so retraining just means re-running
  `train.py` — no need to restart the API.
- CORS is open on the backend so Streamlit (different port) can call it directly.
