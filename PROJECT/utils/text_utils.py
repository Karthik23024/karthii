import re


def normalize_text(text: str) -> str:
    """Clean and normalize resume text for analysis."""
    return re.sub(r"\s+", " ", text.strip())
