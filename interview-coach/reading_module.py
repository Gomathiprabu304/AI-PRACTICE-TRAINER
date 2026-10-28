import streamlit as st
import random
from progress_tracker import save_attempt
st.title("AI-Powered LSRW Communication Coach")
st.write("Reading Module — read the passage and answer the questions.")

# Passage bank: mix of general academic and higher-studies topics
passages = [
    {
        "title": "The Value of Time Management",
        "text": """Time management is one of the most important skills a student can develop. 
It is not simply about doing more tasks in less time, but about prioritizing what truly matters. 
Students who plan their day in advance tend to experience less stress and produce better quality work, 
because they are not rushing to complete tasks at the last minute. Effective time management also creates 
space for rest, which is essential for maintaining focus and motivation over a long period of study.""",
        "questions": [
            {
                "question": "According to the passage, what is time management mainly about?",
                "options": ["Doing more tasks quickly", "Prioritizing what truly matters", "Avoiding rest completely", "Working only at night"],
                "answer": "Prioritizing what truly matters",
                "explanation": "The passage clearly states time management 'is not simply about doing more tasks in less time, but about prioritizing what truly matters.'"
            },
            {
                "question": "Why do students who plan in advance experience less stress?",
                "options": ["They study less", "They are not rushing at the last minute", "They skip assignments", "They sleep more"],
                "answer": "They are not rushing at the last minute",
                "explanation": "The passage explains planning ahead means students are 'not rushing to complete tasks at the last minute.'"
            }
        ]
    },
    {
        "title": "Understanding the Statement of Purpose (SOP)",
        "text": """A Statement of Purpose, commonly known as an SOP, is a critical document required by most 
universities during the admission process for higher studies abroad. It allows an applicant to explain their 
academic background, their reasons for choosing a particular course, and their future career goals. Unlike a 
resume, which simply lists facts, an SOP tells a story — it should clearly connect a student's past experiences 
to their future ambitions, convincing the admissions committee of their genuine interest and preparedness.""",
        "questions": [
            {
                "question": "What is the main purpose of an SOP?",
                "options": ["To list all academic marks", "To explain background, course choice, and future goals", "To replace a resume entirely", "To describe hobbies only"],
                "answer": "To explain background, course choice, and future goals",
                "explanation": "The passage states an SOP allows an applicant to explain their 'academic background, their reasons for choosing a particular course, and their future career goals.'"
            },
            {
                "question": "How is an SOP different from a resume, according to the passage?",
                "options": ["An SOP is shorter", "A resume tells a story, an SOP lists facts", "An SOP tells a story, a resume lists facts", "There is no difference"],
                "answer": "An SOP tells a story, a resume lists facts",
                "explanation": "The passage says 'Unlike a resume, which simply lists facts, an SOP tells a story.'"
            }
        ]
    },
    {
        "title": "The Role of Practice in Building Confidence",
        "text": """Confidence is often misunderstood as a natural trait that some people are simply born with. 
In reality, confidence is built gradually through repeated practice and small successes over time. When a person 
repeatedly faces a challenging situation, such as speaking in public or attending interviews, and receives 
constructive feedback, they slowly become more comfortable and capable. This is why consistent, low-pressure 
practice is often more effective at building genuine confidence than occasional high-stakes attempts.""",
        "questions": [
            {
                "question": "According to the passage, how is confidence actually built?",
                "options": ["It is a trait people are born with", "Through gradual practice and small successes", "By avoiding challenges", "Through one major success"],
                "answer": "Through gradual practice and small successes",
                "explanation": "The passage states confidence 'is built gradually through repeated practice and small successes over time.'"
            },
            {
                "question": "What does the passage say is more effective for building confidence?",
                "options": ["High-stakes attempts", "Consistent, low-pressure practice", "Avoiding feedback", "Working alone"],
                "answer": "Consistent, low-pressure practice",
                "explanation": "The passage concludes that 'consistent, low-pressure practice is often more effective at building genuine confidence than occasional high-stakes attempts.'"
            }
        ]
    }
]

# Pick a passage (randomly, or let student choose)
if "current_passage" not in st.session_state:
    st.session_state.current_passage = random.choice(passages)

passage = st.session_state.current_passage

st.subheader(passage["title"])
st.write(passage["text"])

if st.button("🔄 Try a different passage"):
    st.session_state.current_passage = random.choice(passages)
    st.rerun()

st.divider()
st.subheader("Comprehension Questions")

user_answers = {}
for i, q in enumerate(passage["questions"]):
    user_answers[i] = st.radio(q["question"], q["options"], key=f"q_{i}", index=None)

if st.button("Submit Answers"):
    score = 0
    st.subheader("Results")
    for i, q in enumerate(passage["questions"]):
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

    st.subheader(f"Final Score: {score} / {len(passage['questions'])}")

    save_attempt("Reading", {
        "passage": passage["title"],
        "score": score,
        "total": len(passage["questions"])
    })