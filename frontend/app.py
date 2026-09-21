"""
app.py
------
Streamlit frontend for the House Price Prediction project.

Run with:
    streamlit run app.py

Make sure the FastAPI backend (main.py) is running on port 8000 first.
"""

import os
import requests
import streamlit as st

# On Streamlit Cloud, set API_URL in the app's Secrets (Settings > Secrets) to your
# deployed backend, e.g. API_URL = "https://your-app.onrender.com/predict"
API_URL = st.secrets.get("API_URL", os.environ.get("API_URL", "http://localhost:8000/predict"))

st.set_page_config(
    page_title="House Price Predictor",
    page_icon="🏡",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ---------- Custom styling: peach theme ----------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }

    .stApp {
        background: linear-gradient(160deg, #fff3e9 0%, #ffe3cf 45%, #ffd9c2 100%);
    }

    /* Hide default streamlit chrome for a cleaner look */
    #MainMenu, footer, header { visibility: hidden; }

    .block-container {
        padding-top: 1.5rem;
        max-width: 700px;
    }

    .hero {
        text-align: center;
        padding: 1.5rem 1rem 1rem 1rem;
    }
    .hero h1 {
        font-size: clamp(1.6rem, 5vw, 2.3rem);
        font-weight: 800;
        color: #7a3b1e;
        margin: 0 0 0.35rem 0;
    }
    .hero p {
        color: #a3654a;
        font-size: 0.98rem;
        margin: 0;
    }

    .form-card {
        background: #fffaf6;
        border-radius: 20px;
        padding: 1.8rem clamp(1.1rem, 4vw, 2.2rem) 1.4rem clamp(1.1rem, 4vw, 2.2rem);
        box-shadow: 0 14px 36px rgba(199, 108, 56, 0.16);
        border: 1px solid rgba(230, 145, 94, 0.18);
        margin-bottom: 1.3rem;
    }

    .section-label {
        display: flex;
        align-items: center;
        gap: 0.4rem;
        font-weight: 700;
        color: #7a3b1e;
        font-size: 0.98rem;
        margin: 0.2rem 0 0.6rem 0;
        padding-bottom: 0.4rem;
        border-bottom: 2px solid #ffe1cc;
    }

    div[data-testid="stNumberInput"] label,
    div[data-testid="stSelectbox"] label {
        font-size: 0.83rem;
        color: #a3654a;
        font-weight: 600;
    }

    div[data-testid="stNumberInput"] input {
        border-radius: 10px !important;
        border: 1.5px solid #ffd6b8 !important;
        background: #fffdfb !important;
        color: #7a3b1e !important;
        -webkit-text-fill-color: #7a3b1e !important;
    }
    div[data-testid="stNumberInput"] input:focus {
        border-color: #f0834f !important;
        box-shadow: 0 0 0 3px rgba(240, 131, 79, 0.15) !important;
    }
    div[data-testid="stNumberInput"] button {
        border-color: #ffd6b8 !important;
        color: #d9723f !important;
    }

    .stButton { margin-top: 0.6rem; }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #f4a261 0%, #e76f51 100%);
        color: white;
        font-weight: 700;
        font-size: 1.05rem;
        padding: 0.75rem 0;
        border-radius: 14px;
        border: none;
        box-shadow: 0 10px 24px rgba(231, 111, 81, 0.35);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 14px 28px rgba(231, 111, 81, 0.45);
    }
    .stButton>button:active {
        transform: translateY(0px);
    }

    .result-card {
        background: linear-gradient(135deg, #f4a261 0%, #e76f51 60%, #d9534f 100%);
        border-radius: 20px;
        padding: 1.8rem 1.2rem;
        text-align: center;
        color: white;
        margin-top: 0.4rem;
        box-shadow: 0 16px 34px rgba(231, 111, 81, 0.35);
    }
    .result-label {
        font-size: 0.85rem;
        opacity: 0.9;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        font-weight: 600;
    }
    .result-value {
        font-size: clamp(1.9rem, 6vw, 2.6rem);
        font-weight: 800;
        margin-top: 0.35rem;
    }
    .result-sub {
        font-size: 0.8rem;
        opacity: 0.85;
        margin-top: 0.4rem;
    }

    .footer-note {
        text-align: center;
        color: #b6764f;
        font-size: 0.78rem;
        margin-top: 1rem;
        opacity: 0.8;
    }

    /* Responsive tweaks for small screens */
    @media (max-width: 480px) {
        .form-card { padding: 1.3rem 1rem 1.1rem 1rem; border-radius: 16px; }
        .result-card { padding: 1.4rem 0.9rem; border-radius: 16px; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Header ----------
st.markdown(
    """
    <div class="hero">
        <h1>🏡 House Price Predictor</h1>
        <p>Linear Regression model — enter details below to estimate the price in Lakhs</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------- Input form ----------
with st.form("predict_form"):

    st.markdown('<div class="section-label">📐&nbsp; Property Details</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2, gap="medium")
    with col1:
        area_sqft = st.number_input("Area (sqft)", min_value=100, max_value=10000, value=1500, step=50)
        age_years = st.number_input("Age (years)", min_value=0, max_value=100, value=15)
    with col2:
        distance_km = st.number_input("Distance to City (km)", min_value=0.0, max_value=100.0, value=10.0, step=0.5)
        parking_spaces = st.number_input("Parking Spaces", min_value=0, max_value=5, value=1)

    st.markdown('<div class="section-label" style="margin-top: 1rem;">🛏️&nbsp; Rooms</div>', unsafe_allow_html=True)
    col3, col4 = st.columns(2, gap="medium")
    with col3:
        bedrooms = st.number_input("Bedrooms", min_value=0, max_value=10, value=2)
    with col4:
        bathrooms = st.number_input("Bathrooms", min_value=0, max_value=10, value=1)

    predict_clicked = st.form_submit_button("✨ Predict Price")

    st.markdown("</div>", unsafe_allow_html=True)

# ---------- Prediction ----------
if predict_clicked:
    payload = {
        "Area_sqft": area_sqft,
        "Bedrooms": bedrooms,
        "Bathrooms": bathrooms,
        "Age_years": age_years,
        "Distance_to_City_km": distance_km,
        "Parking_Spaces": parking_spaces,
    }

    try:
        with st.spinner("Estimating price..."):
            response = requests.post(API_URL, json=payload)
            response.raise_for_status()
            result = response.json()

        st.markdown(
            f"""
            <div class="result-card">
                <div class="result-label">Estimated Price</div>
                <div class="result-value">₹ {result['predicted_price_lakhs']} Lakhs</div>
                <div class="result-sub">Based on {area_sqft} sqft · {bedrooms} BHK · {distance_km} km from city</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the backend. Make sure main.py (FastAPI) is running on port 8000.")
    except Exception as e:
        st.error(f"Something went wrong: {e}")

st.markdown('<div class="footer-note">Day 1 · Daily ML Project Series</div>', unsafe_allow_html=True)