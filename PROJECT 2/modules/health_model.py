import os
import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler


class HealthModel:
    """Train a simple risk prediction model and keep preprocessing tools."""

    def __init__(self):
        self.data_path = os.path.join(os.path.dirname(__file__), "..", "data", "health_data.csv")
        self.gender_map = {"Male": 0, "Female": 1}
        self.model = LogisticRegression(max_iter=200)
        self.imputer = SimpleImputer(strategy="median")
        self.scaler = StandardScaler()
        self.feature_names = [
            "Age",
            "Gender",
            "BMI",
            "Blood Pressure",
            "Heart Rate",
            "Temperature",
            "Oxygen",
            "Glucose",
            "Cholesterol",
            "HbA1c",
            "Diabetes",
            "Hypertension",
            "Heart Disease",
        ]
        self.df = self.load_or_generate_data()
        self.train_model()

    def load_or_generate_data(self):
        """Load dataset if it exists; otherwise create and save a synthetic dataset."""
        if os.path.exists(self.data_path):
            return pd.read_csv(self.data_path)

        df = self.generate_synthetic_data(12000)
        os.makedirs(os.path.dirname(self.data_path), exist_ok=True)
        df.to_csv(self.data_path, index=False)
        return df

    def generate_synthetic_data(self, n):
        """Create a simple synthetic health dataset with realistic values."""
        rng = np.random.default_rng(42)
        age = rng.integers(18, 90, size=n)
        gender = rng.choice(["Male", "Female"], size=n, p=[0.48, 0.52])
        bmi = np.round(rng.normal(28, 5, size=n), 1)
        blood_pressure = np.round(rng.normal(125, 20, size=n), 1)
        heart_rate = np.round(rng.normal(75, 12, size=n), 1)
        temperature = np.round(rng.normal(98.4, 0.8, size=n), 1)
        oxygen = np.round(rng.normal(97, 2, size=n), 1)
        glucose = np.round(rng.normal(110, 35, size=n), 1)
        cholesterol = np.round(rng.normal(210, 40, size=n), 1)
        hba1c = np.round(rng.normal(5.8, 1.1, size=n), 1)
        diabetes = rng.choice([0, 1], size=n, p=[0.8, 0.2])
        hypertension = rng.choice([0, 1], size=n, p=[0.7, 0.3])
        heart_disease = rng.choice([0, 1], size=n, p=[0.88, 0.12])

        df = pd.DataFrame(
            {
                "Age": age,
                "Gender": gender,
                "BMI": np.clip(bmi, 16, 45),
                "Blood Pressure": np.clip(blood_pressure, 80, 180),
                "Heart Rate": np.clip(heart_rate, 50, 120),
                "Temperature": np.clip(temperature, 95, 103),
                "Oxygen": np.clip(oxygen, 85, 100),
                "Glucose": np.clip(glucose, 65, 220),
                "Cholesterol": np.clip(cholesterol, 130, 320),
                "HbA1c": np.clip(hba1c, 4.4, 10.5),
                "Diabetes": diabetes,
                "Hypertension": hypertension,
                "Heart Disease": heart_disease,
            }
        )

        df["Risk"] = df.apply(self.compute_risk_label, axis=1)
        df["Treatments"] = df.apply(self.build_treatments, axis=1)

        # Add a few missing values to show pipeline handling
        for col in ["BMI", "Blood Pressure", "Glucose", "Cholesterol"]:
            mask = rng.random(n) < 0.02
            df.loc[mask, col] = np.nan

        return df

    def compute_risk_label(self, row):
        """Generate a realistic risk label for a data row using weighted health factors."""
        score = 0
        score += 0.03 * (row["Age"] - 40)
        score += 0.06 * (row["Blood Pressure"] - 120)
        score += 0.05 * (row["Glucose"] - 100)
        score += 0.05 * (row["Cholesterol"] - 180)
        score += 0.18 * row["Diabetes"]
        score += 0.17 * row["Hypertension"]
        score += 0.15 * row["Heart Disease"]
        score += 0.04 * max(0, row["BMI"] - 25)
        score += 0.08 * max(0, row["HbA1c"] - 5.7)
        score -= 0.05 * max(0, row["Oxygen"] - 95)

        probability = 1 / (1 + np.exp(-(score - 4.5) / 2.5))
        return int(probability > 0.5)

    def build_treatments(self, row):
        """Create a human-readable set of treatment suggestions for the sample."""
        treatments = []
        if row["Diabetes"] or row["Glucose"] > 140 or row["HbA1c"] > 6.0:
            treatments += ["Reduce Sugar Intake", "Metformin Therapy", "Diet Counseling"]
        if row["Hypertension"] or row["Blood Pressure"] > 135:
            treatments += ["Low Salt Diet", "Blood Pressure Medication", "Daily Walks"]
        if row["Heart Disease"] or row["Cholesterol"] > 230:
            treatments += ["Cholesterol Control", "Cardio Exercise", "Heart Health Check"]
        if row["Oxygen"] < 95 or row["Heart Rate"] > 100:
            treatments += ["Oxygen Monitoring", "Stress Reduction"]
        if not treatments:
            treatments = ["General Check-up", "Healthy Nutrition", "Regular Exercise"]
        return " | ".join(treatments[:5])

    def preprocess(self, input_dict):
        """Transform raw input into the model format."""
        df = pd.DataFrame([input_dict])
        df["Gender"] = df["Gender"].map(self.gender_map)
        df = df[self.feature_names].copy()
        df = pd.DataFrame(self.imputer.transform(df), columns=df.columns)
        df[self.feature_names] = self.scaler.transform(df[self.feature_names])
        return df

    def train_model(self):
        """Train the logistic regression model using the synthetic dataset."""
        data = self.df.copy()
        data["Gender"] = data["Gender"].map(self.gender_map)
        x = data[self.feature_names].copy()
        y = data["Risk"].copy()
        self.imputer.fit(x)
        x_imputed = pd.DataFrame(self.imputer.transform(x), columns=x.columns)
        self.scaler.fit(x_imputed)
        x_scaled = pd.DataFrame(self.scaler.transform(x_imputed), columns=x.columns)
        self.model.fit(x_scaled, y)

    def predict(self, input_dict):
        """Return a risk score and simple label for a patient profile."""
        data = self.preprocess(input_dict)
        probability = float(self.model.predict_proba(data)[0, 1])
        label = "High" if probability >= 0.5 else "Low"
        return probability, label

    def feature_importance(self):
        """Return sorted feature importances from the logistic regression model."""
        coefficients = self.model.coef_[0]
        importance = {
            name: float(coef)
            for name, coef in zip(self.feature_names, coefficients)
        }
        sorted_importance = dict(
            sorted(importance.items(), key=lambda item: abs(item[1]), reverse=True)
        )
        return sorted_importance
