import streamlit as st
import joblib
import numpy as np
import pandas as pd

# --- Load saved objects ---
scaler = joblib.load("scaler.pkl")
encoder = joblib.load("encoder.pkl")
model = joblib.load("model.pkl")
meta = joblib.load("meta.pkl")

cat_cols = meta["categorical"]
num_cols = meta["numeric"]
categories = meta["categories"]

st.set_page_config(page_title="💼 Employee Salary Predictor", layout="centered")

st.title("💼 Employee Salary Prediction App")
st.write("Fill in the details below to predict an employee's salary.")

# --- Collect inputs dynamically ---
inputs = {}

for col in num_cols:
    if "age" in col.lower():
        inputs[col] = st.slider("Age", min_value=18, max_value=65, value=30, step=1)
    elif "experience" in col.lower():
        inputs[col] = st.slider("Years of Experience", min_value=0, max_value=40, value=5, step=1)
    else:
        inputs[col] = st.number_input(f"{col}", value=0.0)

for col in cat_cols:
    options = categories.get(col, [])
    if len(options) > 0:
        inputs[col] = st.selectbox(f"{col}", options)
    else:
        inputs[col] = st.text_input(f"{col}")

# --- Prepare dataframe ---
X_input = pd.DataFrame([inputs])

# --- Apply preprocessing ---
X_num = scaler.transform(X_input[num_cols])
X_cat = encoder.transform(X_input[cat_cols])

X_processed = np.hstack([X_num, X_cat])

# --- Predict ---
if st.button("🔮 Predict Salary"):
    prediction = model.predict(X_processed)[0]
    st.success(f"💰 Predicted Salary: **₹ {prediction:,.2f}**")
