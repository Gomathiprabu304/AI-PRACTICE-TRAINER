import streamlit as st
from progress_tracker import save_attempt

st.title("AI-Powered LSRW Communication Coach")
st.subheader("Reading Practice")
st.write("Choose a passage, read it carefully, and answer the questions.")

passages = [
    {
        "title": "The Value of Time Management",
        "text": "Time management is one of the most important skills a student can develop. It is not simply about doing more tasks in less time, but about prioritizing what truly matters. Students who plan their day in advance tend to experience less stress and produce better quality work, because they are not rushing to complete tasks at the last minute. Effective time management also creates space for rest, which is essential for maintaining focus and motivation over a long period of study.",
        "questions": [
            {
                "question": "According to the passage, what is time management mainly about?",
                "options": ["Doing more tasks quickly", "Prioritizing what truly matters", "Avoiding rest completely", "Working only at night"],
                "answer": "Prioritizing what truly matters",
                "explanation": "The passage says time management is not simply about doing more tasks in less time, but about prioritizing what truly matters."
            },
            {
                "question": "Why do students who plan in advance experience less stress?",
                "options": ["They study less", "They are not rushing at the last minute", "They skip assignments", "They sleep more"],
                "answer": "They are not rushing at the last minute",
                "explanation": "The passage explains that planning ahead means students are not rushing to complete tasks at the last minute."
            }
        ]
    },
    {
        "title": "Understanding the Statement of Purpose (SOP)",
        "text": "A Statement of Purpose, commonly known as an SOP, is a critical document required by most universities during the admission process for higher studies abroad. It allows an applicant to explain their academic background, their reasons for choosing a particular course, and their future career goals. Unlike a resume, which simply lists facts, an SOP tells a story. It should clearly connect a student's past experiences to their future ambitions, convincing the admissions committee of their genuine interest and preparedness.",
        "questions": [
            {
                "question": "What is the main purpose of an SOP?",
                "options": ["To list all academic marks", "To explain background, course choice, and future goals", "To replace a resume entirely", "To describe hobbies only"],
                "answer": "To explain background, course choice, and future goals",
                "explanation": "The passage states that an SOP allows an applicant to explain their academic background, their reasons for choosing a course, and their future career goals."
            },
            {
                "question": "How is an SOP different from a resume, according to the passage?",
                "options": ["An SOP is shorter", "A resume tells a story, an SOP lists facts", "An SOP tells a story, a resume lists facts", "There is no difference"],
                "answer": "An SOP tells a story, a resume lists facts",
                "explanation": "The passage says that unlike a resume, which simply lists facts, an SOP tells a story."
            }
        ]
    },
    {
        "title": "The Role of Practice in Building Confidence",
        "text": "Confidence is often misunderstood as a natural trait that some people are simply born with. In reality, confidence is built gradually through repeated practice and small successes over time. When a person repeatedly faces a challenging situation, such as speaking in public or attending interviews, and receives constructive feedback, they slowly become more comfortable and capable. This is why consistent, low-pressure practice is often more effective at building genuine confidence than occasional high-stakes attempts.",
        "questions": [
            {
                "question": "According to the passage, how is confidence actually built?",
                "options": ["It is a trait people are born with", "Through gradual practice and small successes", "By avoiding challenges", "Through one major success"],
                "answer": "Through gradual practice and small successes",
                "explanation": "The passage states that confidence is built gradually through repeated practice and small successes over time."
            },
            {
                "question": "What does the passage say is more effective for building confidence?",
                "options": ["High-stakes attempts", "Consistent, low-pressure practice", "Avoiding feedback", "Working alone"],
                "answer": "Consistent, low-pressure practice",
                "explanation": "The passage concludes that consistent, low-pressure practice is often more effective than occasional high-stakes attempts."
            }
        ]
    },
    {
        "title": "Why Students Choose to Study Abroad",
        "text": "Many students choose to study abroad to gain exposure to new teaching methods, advanced laboratories, and diverse cultures. Studying in another country also builds independence, because students must manage their own money, time, and daily routines. However, it requires careful planning. Students need to research universities, prepare strong applications, and arrange funding well before the deadlines. Those who plan early usually find the process less stressful.",
        "questions": [
            {
                "question": "According to the passage, what does studying abroad build?",
                "options": ["Independence", "Free tuition", "Shorter degrees", "Easier exams"],
                "answer": "Independence",
                "explanation": "The passage says studying in another country builds independence, because students manage their own money, time, and routines."
            },
            {
                "question": "Why should students plan early?",
                "options": ["So the process is less stressful", "Because exams are cancelled", "Because classes start early", "To avoid paying fees"],
                "answer": "So the process is less stressful",
                "explanation": "The passage says that those who plan early usually find the process less stressful."
            },
            {
                "question": "Which of these is NOT mentioned as a benefit of studying abroad?",
                "options": ["Advanced laboratories", "New teaching methods", "Diverse cultures", "Guaranteed jobs"],
                "answer": "Guaranteed jobs",
                "explanation": "The passage mentions teaching methods, laboratories, and cultures. It never mentions guaranteed jobs."
            }
        ]
    },
    {
        "title": "Tips for a Successful Interview",
        "text": "A successful interview begins long before the day itself. Candidates should research the organisation, understand the role, and practise answers to common questions aloud. On the day, arriving early, dressing neatly, and listening carefully to each question create a good impression. When answering, it is better to give clear, structured replies than long, unfocused ones. If a candidate does not know an answer, honestly saying so and explaining how they would find it is better than guessing.",
        "questions": [
            {
                "question": "When does a successful interview begin?",
                "options": ["On the day of the interview", "Long before the day itself", "When the first question is asked", "After the results"],
                "answer": "Long before the day itself",
                "explanation": "The passage opens by saying a successful interview begins long before the day itself."
            },
            {
                "question": "What kind of answers does the passage recommend?",
                "options": ["Long and detailed ones", "Clear, structured replies", "Very short answers", "Memorised speeches"],
                "answer": "Clear, structured replies",
                "explanation": "The passage says it is better to give clear, structured replies than long, unfocused ones."
            },
            {
                "question": "What should a candidate do if they do not know an answer?",
                "options": ["Guess confidently", "Stay silent", "Say so honestly and explain how they would find it", "Change the topic"],
                "answer": "Say so honestly and explain how they would find it",
                "explanation": "The passage says honestly saying so and explaining how they would find the answer is better than guessing."
            }
        ]
    },
    {
        "title": "How to Write an Effective Email",
        "text": "A professional email should be short, polite, and clear. The subject line must tell the reader what the email is about. The opening should state the purpose in one sentence, and the body should give only the necessary details. Ending with a clear request, such as asking for a reply by a specific date, helps the reader know what to do next. Finally, checking spelling and grammar before sending shows care and respect.",
        "questions": [
            {
                "question": "What should the subject line do?",
                "options": ["Be as long as possible", "Tell the reader what the email is about", "Contain a greeting", "Stay empty"],
                "answer": "Tell the reader what the email is about",
                "explanation": "The passage says the subject line must tell the reader what the email is about."
            },
            {
                "question": "What helps the reader know what to do next?",
                "options": ["A long introduction", "Many attachments", "A clear request at the end", "A funny opening"],
                "answer": "A clear request at the end",
                "explanation": "The passage says ending with a clear request, such as asking for a reply by a specific date, helps the reader know what to do next."
            },
            {
                "question": "Why should you check spelling and grammar before sending?",
                "options": ["It makes the email longer", "It shows care and respect", "It is required by law", "It hides the subject"],
                "answer": "It shows care and respect",
                "explanation": "The passage says checking spelling and grammar before sending shows care and respect."
            }
        ]
    }
]

titles = [p["title"] for p in passages]
choice = st.selectbox("Choose a passage", titles)
passage = next(p for p in passages if p["title"] == choice)

st.subheader(passage["title"])
st.write(passage["text"])

st.divider()
st.subheader("Comprehension Questions")

user_answers = {}
for i, q in enumerate(passage["questions"]):
    user_answers[i] = st.radio(
        f"Q{i + 1}. {q['question']}",
        q["options"],
        key=f"{choice}_{i}",
        index=None,
    )

if st.button("Submit Answers"):
    score = 0
    st.subheader("Results")
    for i, q in enumerate(passage["questions"]):
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

    st.subheader(f"Final Score: {score} / {len(passage['questions'])}")

    save_attempt("Reading", {
        "passage": passage["title"],
        "score": score,
        "total": len(passage["questions"]),
    })