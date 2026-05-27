import streamlit as st
import joblib
import pandas as pd
from extractor import extract_features

# Load model
try:
    model = joblib.load('phishing_model.pkl')
except FileNotFoundError:
    st.error("⚠️ Run 'python train.py' in your terminal first to calibrate the new features.")
    st.stop()

st.set_page_config(page_title="Advanced Phishing URL Detector", page_icon="🛡️")
st.title("🛡️ Enterprise Phishing URL Analysis System")

user_url = st.text_input("Enter URL to scan:", placeholder="example.com/login")

if st.button("Run Threat Scan"):
    if user_url.strip() == "":
        st.warning("Please enter a URL to analyze.")
    else:
        with st.spinner("Calculating adversarial vectors..."):
            features = extract_features(user_url)
            features_df = pd.DataFrame([features])
            
            # Predict mathematical probabilities
            prediction = model.predict(features_df)[0]
            probability = model.predict_proba(features_df)[0]
            
            safe_score = probability[0] * 100
            phish_score = probability[1] * 100
            
            st.write("---")
            
            # 3-Tier Security Determination Matrix
            if prediction == 1:
                st.error(f"🚨 **MALICIOUS: Phishing Threat Detected!**")
                st.metric(label="Malicious Indicator Confidence", value=f"{phish_score:.1f}%")
                st.progress(int(phish_score))
                
            elif prediction == 0 and safe_score < 85:
                # The model guessed "Safe" but is uncertain (like your 70% scenario)
                st.warning(f"⚠️ **SUSPICIOUS: Unverified / Low Confidence URL**")
                st.write(f"The system calculated this link as **{safe_score:.1f}% safe**, which does not meet standard enterprise safety baselines (>85%). Avoid interacting with credentials here.")
                st.metric(label="Safety Score (Below Threshold)", value=f"{safe_score:.1f}%")
                st.progress(int(safe_score))
                
            else:
                st.success(f"💚 **VERIFIED SAFE: Highly Confident clean domain.**")
                st.metric(label="System Safety Score", value=f"{safe_score:.1f}%")
                st.progress(int(safe_score))

            with st.expander("Telemetry Structural Data"):
                st.json(features)