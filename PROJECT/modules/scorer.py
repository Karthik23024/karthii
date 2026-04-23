import re

SECTION_WEIGHTS = {
    "Summary": 15,
    "Education": 15,
    "Experience": 25,
    "Skills": 20,
    "Projects": 10,
}


def score_resume(analysis: dict) -> tuple[int, int]:
    score = 0
    for section in analysis["sections_found"]:
        score += SECTION_WEIGHTS.get(section, 5)

    score += min(len(analysis["skills_found"]) * 4, 20)
    score += min(analysis["metrics_count"] * 5, 15)
    score -= min(analysis["grammar_issues"] * 4, 20)

    if analysis["job_match_score"] is not None:
        score += min(analysis["job_match_score"] * 5, 10)

    if analysis["weak_action_phrases"]:
        score -= 5

    score = max(5, min(100, int(score)))

    ats_score = 50
    ats_score += min(len(analysis["skills_found"]) * 3, 20)
    ats_score += 10 if "Skills" in analysis["sections_found"] else 0
    ats_score += 10 if "Experience" in analysis["sections_found"] else 0
    ats_score += 10 if "Education" in analysis["sections_found"] else 0
    ats_score -= min(analysis["grammar_issues"] * 3, 20)
    ats_score = max(20, min(100, int(ats_score)))

    return score, ats_score
