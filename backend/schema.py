from pydantic import BaseModel


class HouseFeatures(BaseModel):
    Area_sqft: float
    Bedrooms: int
    Bathrooms: int
    Age_years: int
    Distance_to_City_km: float
    Parking_Spaces: int


class PredictionResponse(BaseModel):
    predicted_price_lakhs: float
