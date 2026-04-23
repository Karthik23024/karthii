# AI Resume Analyzer (SmartScan)

An AI-powered resume analyzer that accepts PDF and DOCX resumes and delivers strengths, weaknesses, suggestions, a resume score, and an ATS compatibility score.

## Features

- Resume upload for PDF and DOCX files
- Text extraction with `pdfplumber` and `python-docx`
- NLP-driven section detection, skill extraction, and keyword matching
- Grammar and content quality analysis with `spaCy`, `NLTK`, and `TextBlob`
- Resume scoring and ATS optimization recommendations
- Streamlit UI for quick upload and result display

## Project Structure

- `app.py` — main Streamlit application
- `modules/resume_parser.py` — file parsing and text extraction
- `modules/analyzer.py` — NLP analysis and resume inspection
- `modules/scorer.py` — scoring logic and ATS heuristics
- `modules/suggestions.py` — actionable improvement suggestions
- `samples/` — sample resume files for testing
- `requirements.txt` — dependencies

## Setup

1. Create a virtual environment:

```bash
python -m venv .venv
```

2. Activate the virtual environment:

```bash
# Windows PowerShell
.venv\Scripts\Activate.ps1

# Windows CMD
.venv\Scripts\activate.bat
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Download the spaCy English model:

```bash
python -m spacy download en_core_web_sm
```

## Run

```bash
streamlit run app.py
```

## Notes

- The app accepts both PDF and DOCX resumes.
- Use the sample resumes in `samples/` to verify parsing and scoring.
- The application provides a score breakdown and improvement suggestions.
