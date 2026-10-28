import streamlit as st
from progress_tracker import save_attempt
import language_tool_python

st.title("AI-Powered LSRW Communication Coach")
st.write("Speaking Module — helping students build Listening, Speaking, Reading, and Writing confidence.")

# Load the grammar checker (this may take a few seconds the first time)
tool = language_tool_python.LanguageTool('en-US')

user_text = st.text_area("Type your self-introduction here:")

if st.button("Check my intro"):
    if user_text.strip() == "":
        st.warning("Please type something first.")
    else:
        # Grammar check
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

        # Structure check
        st.subheader("Structure Feedback:")

        text_lower = user_text.lower()

        education_keywords = ["studying", "student", "degree", "college", "university", "year", "cse", "engineering", "b.e", "b.tech"]
        skills_keywords = ["skill", "python", "java", "ai", "machine learning", "web development", "programming", "experience", "worked", "learned"]
        goals_keywords = ["goal", "aim", "aspire", "want to", "hope to", "looking forward", "career", "future", "become"]

        has_education = any(word in text_lower for word in education_keywords)
        has_skills = any(word in text_lower for word in skills_keywords)
        has_goals = any(word in text_lower for word in goals_keywords)

        missing = []
        if not has_education:
            missing.append("Education background (e.g., your course, year, college)")
        if not has_skills:
            missing.append("Skills or experience (e.g., what you know or have worked on)")
        if not has_goals:
            missing.append("Goals or career aspirations (e.g., what you want to achieve)")

        if not missing:
            st.success("Great! Your response covers education, skills, and goals.")
        else:
            st.warning("Your response is missing the following:")
            for item in missing:
                st.write(f"⚠️ {item}")
                        # Save this attempt to progress tracking
        save_attempt("Writing", {
            "grammar_issues": len(matches),
            "missing_structure": missing
        })