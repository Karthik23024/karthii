import streamlit as st

from modules.health_model import HealthModel
from modules.recommender import recommend_treatments
from modules.explanations import explain_risk

st.set_page_config(page_title="Medicine Recommender System", layout="centered")
st.title("Medicine Recommender System")
st.write("Use simple patient details to see risk prediction, treatment recommendations, and a plain-language explanation.")

model = HealthModel()


def parse_float(value):
    if value is None or value == "":
        return None
    try:
        return float(value)
    except ValueError:
        return None


def parse_int(value):
    if value is None or value == "":
        return None
    try:
        return int(value)
    except ValueError:
        return None


def parse_binary(value):
    if value == "Yes":
        return 1
    if value == "No":
        return 0
    return None

with st.form("patient_form"):
    age = st.text_input("Age", value="", placeholder="Enter age")
    gender = st.selectbox("Gender", ["", "Male", "Female"])
    blood_pressure = st.selectbox("Blood Pressure", ["", "Low", "High"])
    heart_rate = st.selectbox("Heart Rate", ["", "Low", "High"])
    temperature = st.text_input("Temperature (°F)", value="", placeholder="Enter temperature")
    symptoms = st.multiselect("Symptoms", ["Fever", "Cold", "Cough", "Headache"])
    diabetes = st.selectbox("Diabetes", ["", "No", "Yes"])
    hypertension = st.selectbox("Hypertension", ["", "No", "Yes"])
    heart_disease = st.selectbox("Heart Disease", ["", "No", "Yes"])

    submitted = st.form_submit_button("Predict Risk")

if submitted:
    def map_pressure(value):
        if value == "High":
            return 150.0
        if value == "Low":
            return 90.0
        return None

    def map_rate(value):
        if value == "High":
            return 110.0
        if value == "Low":
            return 60.0
        return None

    profile = {
        "Age": parse_int(age),
        "Gender": gender if gender != "" else None,
        "BMI": None,
        "Blood Pressure": map_pressure(blood_pressure),
        "Heart Rate": map_rate(heart_rate),
        "Temperature": parse_float(temperature),
        "Oxygen": None,
        "Glucose": None,
        "Cholesterol": None,
        "HbA1c": None,
        "Diabetes": parse_binary(diabetes),
        "Hypertension": parse_binary(hypertension),
        "Heart Disease": parse_binary(heart_disease),
        "Symptoms": symptoms,
    }

    required_fields = {
        "Age": profile["Age"],
        "Gender": profile["Gender"],
        "Blood Pressure": profile["Blood Pressure"],
        "Heart Rate": profile["Heart Rate"],
        "Temperature": profile["Temperature"],
        "Diabetes": profile["Diabetes"],
        "Hypertension": profile["Hypertension"],
        "Heart Disease": profile["Heart Disease"],
    }
    missing_fields = [name for name, value in required_fields.items() if value is None]

    if missing_fields:
        st.error(
            f"Please fill in the following fields before predicting: {', '.join(missing_fields)}"
        )
    else:
        probability, label = model.predict(profile)
        explanation = explain_risk(profile, label)
        treatments = recommend_treatments(profile)
        importance = model.feature_importance()

        risk_count = probability * 100
        risk_percentage = f"{risk_count:.1f}".rstrip("0").rstrip(".")

        st.subheader("Risk Prediction")
        st.write(f"**Risk Score:** {risk_percentage}% ({label})")
        st.write(f"**Explanation:** {explanation}")

        st.subheader("Treatment Recommendations")
        for item in treatments:
            st.write(f"- {item['treatment']} — {item['score']}")

        st.subheader("Feature Importance")
        excluded = {"HbA1c", "BMI", "Oxygen", "Glucose"}
        visible = [(k, v) for k, v in importance.items() if k not in excluded]
        for feature, weight in visible[:5]:
            st.write(f"- {feature}: {round(weight, 3)}")
