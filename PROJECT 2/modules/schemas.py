from pydantic import BaseModel


class PatientData(BaseModel):
    Age: int
    Gender: str
    BMI: float
    Blood_Pressure: float
    Heart_Rate: float
    Temperature: float
    Oxygen: float
    Glucose: float
    Cholesterol: float
    HbA1c: float
    Diabetes: int
    Hypertension: int
    Heart_Disease: int

    class Config:
        allow_population_by_field_name = True
        fields = {
            "Blood_Pressure": "Blood Pressure",
            "Heart_Disease": "Heart Disease",
        }
