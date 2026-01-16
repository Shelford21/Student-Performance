import streamlit as st
import pandas as pd
import numpy as np
import joblib

# ======================
# Load Model & Scaler
# ======================
model = joblib.load("model.pkl")
scaler = joblib.load("scaler.pkl")

# ======================
# Page Config
# ======================
st.set_page_config(
    page_title="Student Dropout Early Warning System",
    layout="centered"
)

st.title("🎓 Student Dropout Early Warning System")
st.write(
    "A decision-support tool to identify students who may require early academic intervention."
)

# ======================
# Sidebar - Input
# ======================
st.sidebar.header("Student Profile")

age = st.sidebar.number_input(
    "Age at Enrollment",
    min_value=15,
    max_value=60,
    value=20
)#Umur saat mahasiswa pertama kali masuk

admission_grade = st.sidebar.number_input(
    "Admission Grade",
    min_value=0.0,
    max_value=200.0,
    value=120.0
) #Nilai saat diterima masuk perguruan tinggi

units_enrolled = st.sidebar.number_input(
    "Curricular Units Enrolled (Semester 1)",
    min_value=0,
    max_value=20,
    value=6
)#Jumlah mata kuliah yang diambil pada semester pertama

units_approved = st.sidebar.number_input(
    "Curricular Units Approved (Semester 1)",
    min_value=0,
    max_value=20,
    value=5
)#Jumlah mata kuliah yang lulus pada semester pertama

avg_grade = st.sidebar.number_input(
    "Average Grade (Semester 1)",
    min_value=0.0,
    max_value=20.0,
    value=12.0
)#Rata-rata nilai pada semester pertama

scholarship = st.sidebar.selectbox(
    "Scholarship Holder",
    options=[0, 1],
    format_func=lambda x: "Yes" if x == 1 else "No"
)#Apakah mahasiswa menerima beasiswa

tuition = st.sidebar.selectbox(
    "Tuition Fees Up to Date",
    options=[0, 1],
    format_func=lambda x: "Yes" if x == 1 else "No"
)#Apakah biaya kuliah sudah dibayar tepat waktu

# ======================
# Prediction
# ======================
if st.button("Predict Dropout Risk"):

    input_data = np.array([[
        age,
        admission_grade,
        units_enrolled,
        units_approved,
        avg_grade,
        scholarship,
        tuition
    ]])

    input_scaled = scaler.transform(input_data)
    dropout_prob = model.predict_proba(input_scaled)[0][1]

    # Risk Level
    if dropout_prob < 0.3:
        risk = "LOW"
        color = "green"
        recommendation = "Continue regular academic monitoring."
    elif dropout_prob < 0.6:
        risk = "MEDIUM"
        color = "orange"
        recommendation = "Recommend academic mentoring and progress review."
    else:
        risk = "HIGH"
        color = "red"
        recommendation = "Immediate academic intervention is strongly recommended."

    # ======================
    # Output
    # ======================
    st.subheader("Prediction Result")

    st.metric(
        label="Dropout Risk Probability",
        value=f"{dropout_prob*100:.2f}%"
    )

    st.markdown(
        f"### Risk Level: <span style='color:{color}'>{risk}</span>",
        unsafe_allow_html=True
    )

    st.write("### Recommendation")
    st.info(recommendation)
