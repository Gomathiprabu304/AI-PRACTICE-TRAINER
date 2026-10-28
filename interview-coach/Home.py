import streamlit as st

st.set_page_config(page_title="LSRW Communication Coach", page_icon="🎓")

st.title("AI-Powered LSRW Communication Coach")
st.subheader("Practise Listening, Speaking, Reading and Writing")

st.write("Welcome! Use the menu on the left to choose a skill to practise.")
st.write("This is a coach, not a test. You get corrections, explanations, and unlimited tries.")

st.markdown("""
- **Listening**: listen to an audio clip and answer questions
- **Speaking**: record your voice and get grammar and filler-word feedback
- **Reading**: read a passage and answer questions
- **Writing**: type a response and check grammar and structure
""")