import streamlit as st
import pyttsx3
import random
import os
from progress_tracker import save_attempt

st.title("AI-Powered LSRW Communication Coach")
st.write("Listening Module — listen to the audio and answer the questions.")

clips = [
    {
        "title": "Clip 1: Campus Library Hours",
        "script": "The university library is open from eight in the morning until ten at night on weekdays. On weekends, it closes early at six in the evening. Students are advised to carry their ID cards to enter.",
        "questions": [
            {
                "question": "What time does the library open on weekdays?",
                "options": ["Six in the morning", "Eight in the morning", "Ten in the morning", "Nine in the morning"],
                "answer": "Eight in the morning",
                "explanation": "The audio states the library is open from eight in the morning until ten at night on weekdays."
            },
            {
                "question": "What do students need to carry to enter the library?",
                "options": ["A laptop", "A library book", "Their ID card", "A pen"],
                "answer": "Their ID card",
                "explanation": "The audio says students are advised to carry their ID cards to enter."
            }
        ]
    },
    {
        "title": "Clip 2: Visa Interview Reminder",
        "script": "Applicants attending their visa interview should arrive thirty minutes early. They must bring their passport, admission letter, and financial documents. Mobile phones are not allowed inside the interview room.",
        "questions": [
            {
                "question": "How early should applicants arrive for the interview?",
                "options": ["Fifteen minutes early", "Thirty minutes early", "One hour early", "On time, not early"],
                "answer": "Thirty minutes early",
                "explanation": "The audio states applicants should arrive thirty minutes early."
            },
            {
                "question": "What is not allowed inside the interview room?",
                "options": ["Passport", "Admission letter", "Mobile phones", "Financial documents"],
                "answer": "Mobile phones",
                "explanation": "The audio says mobile phones are not allowed inside the interview room."
            }
        ]
    }
]

@st.cache_data
def generate_audio(text, filename):
    engine = pyttsx3.init()
    engine.save_to_file(text, filename)
    engine.runAndWait()
    return filename

if "current_clip" not in st.session_state:
    st.session_state.current_clip = random.choice(clips)

clip = st.session_state.current_clip

st.subheader(clip["title"])

audio_path = f"temp_audio_{clips.index(clip)}.mp3"
if not os.path.exists(audio_path):
    generate_audio(clip["script"], audio_path)

st.audio(audio_path)
st.caption("Click play to listen. You can replay it as many times as you need.")

if st.button("🔄 Try a different clip"):
    st.session_state.current_clip = random.choice(clips)
    st.rerun()

st.divider()
st.subheader("Comprehension Questions")

user_answers = {}
for i, q in enumerate(clip["questions"]):
    user_answers[i] = st.radio(q["question"], q["options"], key=f"lq_{i}", index=None)

if st.button("Submit Answers"):
    score = 0
    st.subheader("Results")
    for i, q in enumerate(clip["questions"]):
        selected = user_answers[i]
        if selected == q["answer"]:
            st.success(f"Q{i+1}: Correct! ✅")
            score += 1
        else:
            st.error(f"Q{i+1}: Incorrect ❌")
            st.write(f"Your answer: {selected if selected else 'No answer selected'}")
            st.write(f"Correct answer: {q['answer']}")
            st.write(f"Explanation: {q['explanation']}")
        st.write("---")

    st.subheader(f"Final Score: {score} / {len(clip['questions'])}")

    save_attempt("Listening", {
        "clip": clip["title"],
        "score": score,
        "total": len(clip["questions"])
    })