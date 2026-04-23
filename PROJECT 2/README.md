# Medicine Recommender System

A beginner-friendly AI project that predicts patient health risk, recommends treatments, and explains results in simple language.

## Project Structure

- `app.py` - Streamlit frontend UI for input and display.
- `backend.py` - FastAPI backend with risk prediction and treatment endpoints.
- `modules/health_model.py` - Data generation, preprocessing, and model training.
- `modules/recommender.py` - Rule-based treatment recommendation logic.
- `modules/explanations.py` - Simple explanation text for predictions.
- `modules/schemas.py` - API input schema definitions.
- `data/` - Synthetic dataset created on first run.
- `requirements.txt` - Python dependencies.

## Setup

1. Create and activate a Python environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the Backend

Start the FastAPI server:

```bash
uvicorn backend:app --reload
```

## Run the Frontend

In another terminal, start Streamlit:

```bash
streamlit run app.py
```

## How it Works

- The backend trains a simple logistic regression model on synthetic health data.
- The frontend collects patient measurements.
- The backend returns a risk score, risk label, explanation, and treatment recommendations.

## Notes

- The dataset is generated automatically into `data/health_data.csv`.
- The code is intentionally simple and easy to read.
