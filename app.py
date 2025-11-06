import streamlit as st
import pandas as pd
import numpy as np
import pickle

# Load the fixed model (you'll upload model_fixed.pkl next)
with open('model_fixed.pkl', 'rb') as f:
    model_fixed = pickle.load(f)

st.title("🇿🇦 FairHire SA - Bias-Free CV Screener")

st.write("Enter CV details for fair screening. This uses a bias-mitigated model trained on SA-specific data.")

# User inputs
gender = st.selectbox("Gender", ["Male", "Female"])
race = st.selectbox("Race", ["White", "Black", "Coloured", "Indian"])
address_type = st.selectbox("Address Type", ["Urban", "Township"])
experience = st.number_input("Experience Years", min_value=0, max_value=20, value=5)
education = st.selectbox("Education Level (1=High School, 4=Postgrad)", [1, 2, 3, 4])

if st.button("Screen CV Fairly"):
    # Prepare input DataFrame matching training columns
    input_data = {
        'experience_years': [experience],
        'education_level': [education],
        'gender_Female': [1 if gender == 'Female' else 0],
        'race_Black': [1 if race == 'Black' else 0],
        'race_Coloured': [1 if race == 'Coloured' else 0],
        'race_Indian': [1 if race == 'Indian' else 0],
        'address_type_Township': [1 if address_type == 'Township' else 0]
    }
    input_df = pd.DataFrame(input_data)

    # Predict
    prediction = model_fixed.predict(input_df)[0]
    prob = model_fixed.predict_proba(input_df)[0][1] * 100  # Probability of hire

    if prediction == 1:
        st.success(f"🎉 Recommended for Hire! Confidence: {prob:.1f}%")
    else:
        st.warning(f"❌ Not Recommended. Confidence: {prob:.1f}%")
    st.write("Explanation: This model has been audited and fixed for biases related to gender, race, and location in South African contexts. No unfair penalties applied.")
