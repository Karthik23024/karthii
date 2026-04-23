def explain_risk(profile, risk_label):
    """Create a plain-language explanation based on key health values."""
    def numeric(value, default=0):
        return value if isinstance(value, (int, float)) else default

    reasons = []
    if numeric(profile.get("Glucose")) > 140 or numeric(profile.get("HbA1c")) > 6.0:
        reasons.append("high glucose")
    if numeric(profile.get("Blood Pressure")) > 135 or profile.get("Hypertension", 0) == 1:
        reasons.append("elevated blood pressure")
    if numeric(profile.get("Cholesterol")) > 220 or profile.get("Heart Disease", 0) == 1:
        reasons.append("cholesterol or heart risk")
    if numeric(profile.get("Oxygen"), 100) < 95:
        reasons.append("low oxygen levels")
    if numeric(profile.get("BMI")) > 30:
        reasons.append("high BMI")
    if numeric(profile.get("Age")) > 65:
        reasons.append("age-related risk")

    symptoms = profile.get("Symptoms", []) or []
    if "Fever" in symptoms:
        reasons.append("fever")
    if "Cough" in symptoms or "Cold" in symptoms:
        reasons.append("respiratory symptoms")
    if "Headache" in symptoms:
        reasons.append("headache")

    if not reasons:
        if risk_label == "Low":
            return "Most health markers are in a normal range, so risk is lower."
        return "Risk is moderate due to general profiling."

    main_reasons = " and ".join(reasons[:2])
    return f"{main_reasons.capitalize()} increased the risk."