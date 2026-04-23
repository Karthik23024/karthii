def recommend_treatments(profile):
    """Return top treatments using simple rules and weighted scores."""
    def numeric(value, default=0):
        return value if isinstance(value, (int, float)) else default

    scores = {}
    glucose = numeric(profile.get("Glucose"))
    bp = numeric(profile.get("Blood Pressure"))
    chol = numeric(profile.get("Cholesterol"))
    hba1c = numeric(profile.get("HbA1c"))
    oxygen = numeric(profile.get("Oxygen"), 100)
    diabetes = profile.get("Diabetes", 0)
    hypertension = profile.get("Hypertension", 0)
    heart_disease = profile.get("Heart Disease", 0)

    if diabetes or glucose > 130 or hba1c > 6.0:
        scores["Lifestyle Change"] = 0.94
        scores["Sugar Control Plan"] = 0.88
        scores["Metformin Therapy"] = 0.82

    if hypertension or bp > 135:
        scores["Low Salt Diet"] = 0.91
        scores["Blood Pressure Medication"] = 0.86

    if heart_disease or chol > 220:
        scores["Heart Healthy Exercise"] = 0.89
        scores["Cholesterol Control"] = 0.84

    if oxygen < 95 or numeric(profile.get("Heart Rate", 0)) > 100:
        scores["Oxygen Monitoring"] = 0.80
        scores["Stress Reduction"] = 0.76

    symptoms = profile.get("Symptoms", []) or []
    if "Fever" in symptoms:
        scores["Fever Check"] = 0.78
    if "Cough" in symptoms or "Cold" in symptoms:
        scores["Respiratory Care"] = 0.75
    if "Headache" in symptoms:
        scores["Pain Management"] = 0.72

    if not scores:
        scores = {
            "General Check-up": 0.80,
            "Healthy Diet": 0.77,
            "Regular Exercise": 0.74,
        }

    ranked = sorted(scores.items(), key=lambda item: item[1], reverse=True)[:5]
    return [{"treatment": name, "score": round(value, 2)} for name, value in ranked]
