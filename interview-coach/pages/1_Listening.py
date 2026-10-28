import os
import streamlit as st
import pyttsx3
from progress_tracker import save_attempt

st.title("AI-Powered LSRW Communication Coach")
st.subheader("Listening Practice")
st.write("Choose a clip, listen carefully, and answer the questions.")

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
    },
    {
        "title": "Clip 3: Admission Deadline Notice",
        "script": "The admissions office announces that applications for the autumn intake close on the fifteenth of March. Students must upload their transcripts, two recommendation letters, and a statement of purpose. Late applications will not be accepted.",
        "questions": [
            {
                "question": "When do applications for the autumn intake close?",
                "options": ["First of March", "Fifteenth of March", "Fifteenth of April", "Thirtieth of March"],
                "answer": "Fifteenth of March",
                "explanation": "The audio says applications close on the fifteenth of March."
            },
            {
                "question": "How many recommendation letters are required?",
                "options": ["One", "Two", "Three", "None"],
                "answer": "Two",
                "explanation": "The audio says students must upload two recommendation letters."
            },
            {
                "question": "What will not be accepted?",
                "options": ["Late applications", "Online applications", "Transcripts", "Statements of purpose"],
                "answer": "Late applications",
                "explanation": "The audio ends by saying late applications will not be accepted."
            }
        ]
    },
    {
        "title": "Clip 4: Interview Preparation Advice",
        "script": "Before an interview, you should read about the company and practise your answers aloud. On the day, arrive ten minutes early and keep your documents in a folder. During the interview, listen carefully and answer one question at a time.",
        "questions": [
            {
                "question": "How early should you arrive on the day of the interview?",
                "options": ["Five minutes early", "Ten minutes early", "Thirty minutes early", "One hour early"],
                "answer": "Ten minutes early",
                "explanation": "The audio says to arrive ten minutes early."
            },
            {
                "question": "Where should you keep your documents?",
                "options": ["In a bag", "In your pocket", "In a folder", "On your phone"],
                "answer": "In a folder",
                "explanation": "The audio says to keep your documents in a folder."
            },
            {
                "question": "What should you practise aloud before the interview?",
                "options": ["Your handwriting", "Your answers", "Your signature", "Your questions for the company"],
                "answer": "Your answers",
                "explanation": "The audio says to read about the company and practise your answers aloud."
            }
        ]
    },
    {
        "title": "Clip 5: Lecture Announcement",
        "script": "Tomorrow's lecture on machine learning will be held in Seminar Hall B instead of Room two hundred and four. The session starts at ten thirty in the morning and will last ninety minutes. Please bring your laptops for the practical exercise.",
        "questions": [
            {
                "question": "Where will tomorrow's lecture be held?",
                "options": ["Room 204", "Seminar Hall B", "The library", "The computer lab"],
                "answer": "Seminar Hall B",
                "explanation": "The audio says the lecture will be held in Seminar Hall B instead of Room 204."
            },
            {
                "question": "What time does the session start?",
                "options": ["Nine thirty", "Ten", "Ten thirty", "Eleven thirty"],
                "answer": "Ten thirty",
                "explanation": "The audio says the session starts at ten thirty in the morning."
            },
            {
                "question": "What should students bring?",
                "options": ["Textbooks", "Laptops", "Lunch", "Calculators"],
                "answer": "Laptops",
                "explanation": "The audio asks students to bring their laptops for the practical exercise."
            }
        ]
    },
    {
        "title": "Clip 6: Study Group Plan",
        "script": "The study group will meet every Wednesday at four in the afternoon in the library. This week we will practise IELTS speaking topics. Each member will speak for two minutes and receive feedback from the others.",
        "questions": [
            {
                "question": "When does the study group meet?",
                "options": ["Every Monday at four", "Every Wednesday at four", "Every Wednesday at five", "Every Friday at four"],
                "answer": "Every Wednesday at four",
                "explanation": "The audio says the group meets every Wednesday at four in the afternoon."
            },
            {
                "question": "What will the group practise this week?",
                "options": ["IELTS speaking topics", "IELTS writing tasks", "Mathematics", "Computer programming"],
                "answer": "IELTS speaking topics",
                "explanation": "The audio says that this week they will practise IELTS speaking topics."
            },
            {
                "question": "How long will each member speak?",
                "options": ["One minute", "Two minutes", "Five minutes", "Ten minutes"],
                "answer": "Two minutes",
                "explanation": "The audio says each member will speak for two minutes."
            }
        ]
    }
]


def make_audio(text, filename):
    engine = pyttsx3.init()
    engine.save_to_file(text, filename)
    engine.runAndWait()


titles = [c["title"] for c in clips]
choice = st.selectbox("Choose a clip", titles)
clip_index = titles.index(choice)
clip = clips[clip_index]

audio_path = f"listening_clip_{clip_index + 1}.wav"
if not os.path.exists(audio_path):
    with st.spinner("Preparing the audio..."):
        make_audio(clip["script"], audio_path)

st.subheader(clip["title"])
st.audio(audio_path)
st.caption("Click play to listen. You can replay it as many times as you need.")

st.divider()
st.subheader("Comprehension Questions")

user_answers = {}
for i, q in enumerate(clip["questions"]):
    user_answers[i] = st.radio(
        f"Q{i + 1}. {q['question']}",
        q["options"],
        key=f"listen_{clip_index}_{i}",
        index=None,
    )

if st.button("Submit Answers"):
    score = 0
    st.subheader("Results")
    for i, q in enumerate(clip["questions"]):
        selected = user_answers[i]
        if selected == q["answer"]:
            st.success(f"Q{i + 1}: Correct! ✅")
            score += 1
        else:
            st.error(f"Q{i + 1}: Incorrect ❌")
            st.write(f"Your answer: {selected if selected else 'No answer selected'}")
            st.write(f"Correct answer: {q['answer']}")
            st.write(f"Explanation: {q['explanation']}")
        st.write("---")

    st.subheader(f"Final Score: {score} / {len(clip['questions'])}")

    save_attempt("Listening", {
        "clip": clip["title"],
        "score": score,
        "total": len(clip["questions"]),
    })