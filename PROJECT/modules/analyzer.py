import re
from textblob import TextBlob
import nltk
import spacy
from utils.text_utils import normalize_text

nltk.download("punkt", quiet=True)

SKILLS_LIBRARY = [
    "python", "java", "sql", "excel", "data analysis", "machine learning", "deep learning",
    "nlp", "project management", "communication", "leadership", "cloud", "aws", "azure",
    "tensorflow", "pytorch", "docker", "kubernetes", "react", "node.js", "javascript",
    "git", "linux", "tableau", "power bi", "presentation", "problem solving"
]

WEAK_ACTIONS = [
    "responsible for", "assist", "helped", "supported", "worked on", "participated",
    "duties include", "tasked with", "handled", "managed"
]

STRONG_ACTIONS = [
    "improved", "led", "delivered", "designed", "built", "launched", "managed",
    "optimized", "streamlined", "accelerated", "expanded", "implemented"
]

SECTION_LABELS = {
    "summary": ["summary", "profile", "professional summary", "about me"],
    "education": ["education", "academic background", "qualifications"],
    "experience": ["experience", "professional experience", "work history", "employment"],
    "skills": ["skills", "technical skills", "core skills", "expertise"],
    "projects": ["projects", "portfolio", "selected projects", "research"]
}


def load_spacy_model():
    try:
        return spacy.load("en_core_web_sm")
    except OSError:
        spacy.cli.download("en_core_web_sm")
        return spacy.load("en_core_web_sm")


NLP = load_spacy_model()

JOB_ROLE_KEYWORDS = {
    "Data Analyst": ["data analysis", "sql", "tableau", "power bi", "excel", "data visualization", "reporting"],
    "Data Scientist": ["machine learning", "python", "tensorflow", "pytorch", "nlp", "deep learning", "model"],
    "ML Engineer": ["machine learning", "deep learning", "tensorflow", "pytorch", "docker", "kubernetes", "cloud", "aws", "azure"],
    "Software Engineer": ["python", "java", "javascript", "react", "node.js", "git", "docker", "kubernetes", "linux"],
    "DevOps Engineer": ["docker", "kubernetes", "aws", "azure", "cloud", "linux", "git", "automation"],
    "Product Manager": ["project management", "stakeholders", "strategy", "roadmap", "product", "launch", "communication"],
    "Business Analyst": ["sql", "excel", "data analysis", "reporting", "requirements", "process improvement", "stakeholders"]
}


def detect_sections(text: str):
    lower_text = text.lower()
    found_sections = []
    for section, keywords in SECTION_LABELS.items():
        for keyword in keywords:
            if keyword in lower_text:
                found_sections.append(section.capitalize())
                break
    return found_sections


def extract_skills(text: str):
    lower_text = text.lower()
    found = []
    for skill in SKILLS_LIBRARY:
        if skill in lower_text and skill not in found:
            found.append(skill)
    return found


def recommend_job_roles(text: str, skills: list[str]) -> list[str]:
    lower_text = text.lower()
    scores = {}
    for role, keywords in JOB_ROLE_KEYWORDS.items():
        count = 0
        for keyword in keywords:
            if keyword in lower_text:
                count += 1
        for skill in skills:
            if skill in keywords:
                count += 1
        if count > 0:
            scores[role] = count

    sorted_roles = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    return [role for role, _ in sorted_roles[:3]]


def count_quantified_results(text: str) -> int:
    patterns = [r"\d+%", r"\d+\s+(?:years|months|weeks)", r"\d+\+", r"\d+\s*(?:k|m|million|billion)", r"\d+\s+(?:people|customers|clients|sales|revenue|projects)" ]
    count = 0
    for pattern in patterns:
        count += len(re.findall(pattern, text, flags=re.IGNORECASE))
    return count


def detect_weak_actions(text: str):
    lower_text = text.lower()
    return [phrase for phrase in WEAK_ACTIONS if phrase in lower_text]


def detect_strong_actions(text: str):
    lower_text = text.lower()
    return [phrase for phrase in STRONG_ACTIONS if phrase in lower_text]


def grammar_and_spelling_issues(text: str) -> int:
    blob = TextBlob(text)
    issues = 0
    for sentence in blob.sentences:
        corrected = sentence.correct()
        if str(corrected).strip().lower() != str(sentence).strip().lower():
            issues += 1
    return issues


def analyze_resume(text: str, job_description: str = None) -> dict:
    cleaned = normalize_text(text)
    sections = detect_sections(cleaned)
    skills = extract_skills(cleaned)
    metrics = count_quantified_results(cleaned)
    weak_actions = detect_weak_actions(cleaned)
    strong_actions = detect_strong_actions(cleaned)
    grammar_issues = grammar_and_spelling_issues(cleaned)
    missing_sections = [label.capitalize() for label in SECTION_LABELS if label.capitalize() not in sections]

    strengths = []
    weaknesses = []

    if strong_actions:
        strengths.append(f"Strong action language detected: {', '.join(set(strong_actions))}.")
    else:
        weaknesses.append("Consider using stronger action verbs such as improved, led, designed, or launched.")

    if skills:
        strengths.append(f"Relevant skills found: {', '.join(skills[:8])}.")
    else:
        weaknesses.append("No recognizable skills section detected or skills are not clearly listed.")

    if metrics >= 3:
        strengths.append("Resume includes multiple quantified achievements.")
    elif metrics > 0:
        weaknesses.append("Add more numbers and metrics to strengthen achievements.")
    else:
        weaknesses.append("Add measurable accomplishments with numbers, percentages, or timeframes.")

    if grammar_issues == 0:
        strengths.append("Grammar and spelling appear clean.")
    else:
        weaknesses.append(f"There are approximately {grammar_issues} grammar or spelling issue areas.")

    for section in missing_sections:
        weaknesses.append(f"Missing or unclear section: {section}.")

    if weak_actions:
        weaknesses.append(f"Weak action phrases found: {', '.join(set(weak_actions))}.")

    job_match_score = None
    if job_description:
        job_text = normalize_text(job_description)
        matched_keywords = [skill for skill in skills if skill in job_text]
        job_match_score = len(matched_keywords)
        if matched_keywords:
            strengths.append(f"Job description appears to align with skills: {', '.join(matched_keywords)}.")
        else:
            weaknesses.append("Few or no resume skills match the provided job description.")

    recommended_roles = recommend_job_roles(cleaned, skills)
    if recommended_roles:
        strengths.append(f"Recommended job categories: {', '.join(recommended_roles)}.")

    return {
        "text": cleaned,
        "sections_found": sections,
        "skills_found": skills,
        "metrics_count": metrics,
        "grammar_issues": grammar_issues,
        "weak_action_phrases": weak_actions,
        "strong_action_phrases": strong_actions,
        "missing_sections": missing_sections,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "job_match_score": job_match_score,
        "recommended_roles": recommended_roles,
    }
