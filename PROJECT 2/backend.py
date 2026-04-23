from fastapi import FastAPI
from modules.health_model import HealthModel
from modules.recommender import recommend_treatments
from modules.explanations import explain_risk
from modules.schemas import PatientData

app = FastAPI(title="Medicine Recommender System")
model = HealthModel()


@app.get("/health")
def health():
    """Simple health check for the API."""
    return {"status": "ok", "message": "Medicine Recommender System is ready."}


def map_profile(patient_data):
    """Convert the API input fields into model feature names."""
    profile = patient_data.copy()
    profile["Blood Pressure"] = profile.pop("Blood_Pressure")
    profile["Heart Disease"] = profile.pop("Heart_Disease")
    return profile


@app.post("/predict-risk")
def predict_risk(patient: PatientData):
    """Predict the risk score and a simple risk label."""
    profile = map_profile(patient.dict())
    probability, label = model.predict(profile)
    explanation = explain_risk(profile, label)
    importance = model.feature_importance()
    return {
        "risk_score": round(probability, 2),
        "risk_label": label,
        "explanation": explanation,
        "feature_importance": importance,
    }


@app.post("/recommend")
def recommend(patient: PatientData):
    """Return a short list of treatment recommendations."""
    profile = map_profile(patient.dict())
    treatments = recommend_treatments(profile)
    return {"recommendations": treatments}
