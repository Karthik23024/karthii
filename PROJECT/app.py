import streamlit as st
from modules.resume_parser import extract_text_from_resume
from modules.analyzer import analyze_resume
from modules.scorer import score_resume
from modules.suggestions import generate_suggestions

st.set_page_config(page_title="AI Resume Analyzer (SmartScan)", layout="wide")

st.title("AI Resume Analyzer — SmartScan")
st.markdown("Analyze your resume and receive strengths, weaknesses, suggestions, and ATS optimization feedback.")

uploaded_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"], accept_multiple_files=False)
job_text = None

if uploaded_file is not None:
    with st.spinner("Extracting resume content..."):
        resume_text = extract_text_from_resume(uploaded_file)

    if not resume_text.strip():
        st.error("Could not extract any text from the uploaded resume.")
    else:
        analysis = analyze_resume(resume_text, job_description=job_text)
        score, ats_score = score_resume(analysis)
        suggestions = generate_suggestions(analysis)

        col1, col2 = st.columns([1, 1])
        with col1:
            st.subheader("Resume Score")
            st.progress(score / 100)
            st.metric("Overall Score", f"{score}/100")
            st.metric("ATS Compatibility", f"{ats_score}%")

        with col2:
            st.subheader("Key Resume Insights")
            st.write(f"**Detected sections:** {', '.join(analysis['sections_found'])}")
            st.write(f"**Skills found:** {', '.join(analysis['skills_found'][:12])}")
            st.write(f"**Grammar / spelling issues:** {analysis['grammar_issues']}")
            st.write(f"**Quantified achievements:** {analysis['metrics_count']}")
            if analysis.get('recommended_roles'):
                st.write(f"**Recommended job categories:** {', '.join(analysis['recommended_roles'])}")
            else:
                st.write("**Recommended job categories:** No clear role detected. Add more target keywords.")

        st.markdown("---")
        strength_col, weakness_col = st.columns(2)
        with strength_col:
            st.subheader("Strengths")
            for item in analysis["strengths"]:
                st.write(f"- {item}")

        with weakness_col:
            st.subheader("Weaknesses")
            for item in analysis["weaknesses"]:
                st.write(f"- {item}")

        st.markdown("---")
        st.subheader("Suggestions")
        for suggestion in suggestions:
            st.write(f"- {suggestion}")

        with st.expander("Show extracted resume text"):
            st.text_area("Resume text", value=resume_text, height=300)

else:
    st.info("Upload a PDF or DOCX resume to begin the analysis.")
