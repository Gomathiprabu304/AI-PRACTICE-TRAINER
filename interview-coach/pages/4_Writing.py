import re
import streamlit as st
import language_tool_python
from progress_tracker import save_attempt

st.title("AI-Powered LSRW Communication Coach")
st.subheader("Writing Practice")

@st.cache_resource
def load_grammar_tool():
    return language_tool_python.LanguageTool('en-US')

tool = load_grammar_tool()

STRUCTURE = {
    "Self-introduction": {
        "Education background (your course, year, college)": [
            "studying", "student", "degree", "college", "university", "year",
            "cse", "engineering", "b.e", "b.tech"],
        "Skills or experience (what you know or have worked on)": [
            "skill", "python", "java", "ai", "machine learning", "web development",
            "programming", "experience", "worked", "learned"],
        "Goals or career aspirations (what you want to achieve)": [
            "goal", "aim", "aspire", "want to", "hope to", "looking forward",
            "career", "future", "become"],
    },
    "SOP (Statement of Purpose)": {
        "Your interest in the field (why you chose it)": [
            "passion", "interest", "inspired", "fascinat", "curious", "motivat", "drawn to"],
        "Academic background (degree, marks, coursework)": [
            "bachelor", "b.e", "b.tech", "degree", "cgpa", "gpa", "coursework",
            "graduat", "studied", "semester"],
        "Projects, internships, or research experience": [
            "project", "internship", "research", "experience", "developed",
            "built", "worked", "paper"],
        "Why this university or course": [
            "university", "program", "course", "faculty", "professor",
            "curriculum", "laborator", "lab", "department", "campus"],
        "Career goals (short-term and long-term)": [
            "goal", "career", "aim", "aspire", "future", "long-term",
            "short-term", "plan to", "want to", "hope to", "become"],
    },
}

TIPS = {
    "Self-introduction": "Cover your education, your skills, and your goals. Keep it under one minute when spoken.",
    "SOP (Statement of Purpose)": "A good SOP tells a story: your interest in the field, your background, your projects, why this university and course, and your career goals. Many universities ask for about 500 to 1000 words, so check your university's limit.",
}

def has_any(text, words):
    for w in words:
        if len(w) <= 3:
            pattern = r"\b" + re.escape(w) + r"\b"
        else:
            pattern = r"\b" + re.escape(w)
        if re.search(pattern, text):
            return True
    return False

mode = st.radio("What are you writing?", list(STRUCTURE.keys()), horizontal=True)
st.info(TIPS[mode])

user_text = st.text_area("Type your response here:", height=250)

if st.button("Check my writing"):
    if user_text.strip() == "":
        st.warning("Please type something first.")
    else:
        word_count = len(user_text.split())
        st.write(f"Word count: **{word_count}**")

        with st.spinner("Checking grammar..."):
            matches = tool.check(user_text)

        st.subheader("Grammar Feedback:")
        if len(matches) == 0:
            st.success("No grammar mistakes found! Well done.")
        else:
            st.write(f"Found {len(matches)} issue(s):")
            for m in matches:
                st.write(f"❌ **Issue:** {m.message}")
                st.write(f"   → Suggestion: {', '.join(m.replacements) if m.replacements else 'No suggestion'}")
                st.write("---")

        st.subheader("Structure Feedback:")
        text_lower = user_text.lower()
        missing = []
        for part, words in STRUCTURE[mode].items():
            if has_any(text_lower, words):
                st.write(f"✅ {part}")
            else:
                st.write(f"⚠️ Missing: {part}")
                missing.append(part)

        if not missing:
            st.success("Great! Your response covers every part.")
        else:
            st.warning("Add the missing parts, then check again.")

        save_attempt("Writing", {
            "type": mode,
            "word_count": word_count,
            "grammar_issues": len(matches),
            "missing_structure": missing
        })