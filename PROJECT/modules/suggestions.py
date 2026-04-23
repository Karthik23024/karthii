def generate_suggestions(analysis: dict) -> list[str]:
    suggestions = []

    if "Summary" not in analysis["sections_found"]:
        suggestions.append("Add a concise professional summary at the top of your resume.")

    if "Skills" not in analysis["sections_found"]:
        suggestions.append("Create a dedicated Skills section with clear technical and soft skills.")
    elif len(analysis["skills_found"]) < 5:
        suggestions.append("Expand your skills list with industry keywords relevant to your target role.")

    if analysis["metrics_count"] < 2:
        suggestions.append("Include specific metrics, such as percentages, timeframes, or revenue impact.")

    if analysis["grammar_issues"] > 0:
        suggestions.append("Proofread the resume carefully or use a grammar checker to correct spelling and phrasing.")

    if analysis["weak_action_phrases"]:
        suggestions.append("Replace weak phrases like 'responsible for' or 'helped' with strong action verbs.")

    if analysis["job_match_score"] == 0:
        suggestions.append("Match your resume keywords more closely to the job description for better ATS alignment.")

    if analysis.get("recommended_roles") is not None and not analysis["recommended_roles"]:
        suggestions.append("Your resume does not match a clear job category yet. Add role-specific keywords for your target job.")

    if "Projects" not in analysis["sections_found"]:
        suggestions.append("Add a Projects section with short descriptions of relevant work or accomplishments.")

    if not suggestions:
        suggestions.append("Your resume is strong. Continue refining it with measurable accomplishments and clear formatting.")

    return suggestions
