import streamlit as st
from progress_tracker import save_attempt

st.title("AI-Powered LSRW Communication Coach")
st.subheader("Aptitude and MCQ Practice")
st.write("Pick a topic, answer the questions, and read the step-by-step explanation for any you miss.")

QUESTIONS = {
    "Quantitative": [
        {
            "question": "What is 20% of 250?",
            "options": ["25", "40", "50", "60"],
            "answer": "50",
            "steps": [
                "20% means 20 out of 100, which is 20/100.",
                "Multiply by 250: 20/100 × 250.",
                "250 ÷ 100 = 2.5, and 2.5 × 20 = 50.",
            ],
        },
        {
            "question": "A train travels 120 km in 2 hours. What is its speed?",
            "options": ["40 km/h", "50 km/h", "60 km/h", "70 km/h"],
            "answer": "60 km/h",
            "steps": [
                "Speed = Distance ÷ Time.",
                "Speed = 120 ÷ 2.",
                "Speed = 60 km/h.",
            ],
        },
        {
            "question": "Divide 60 in the ratio 2:3. What is the larger part?",
            "options": ["24", "30", "36", "40"],
            "answer": "36",
            "steps": [
                "Add the ratio parts: 2 + 3 = 5 parts.",
                "One part = 60 ÷ 5 = 12.",
                "The larger part has 3 parts: 3 × 12 = 36.",
            ],
        },
        {
            "question": "An item is bought for 400 rupees and sold for 500 rupees. What is the profit percentage?",
            "options": ["20%", "25%", "30%", "10%"],
            "answer": "25%",
            "steps": [
                "Profit = Selling price − Cost price = 500 − 400 = 100.",
                "Profit % = Profit ÷ Cost price × 100.",
                "Profit % = 100 ÷ 400 × 100 = 25%.",
            ],
        },
        {
            "question": "What is the average of 10, 20, 30, 40 and 50?",
            "options": ["25", "30", "35", "40"],
            "answer": "30",
            "steps": [
                "Add all the numbers: 10 + 20 + 30 + 40 + 50 = 150.",
                "Divide by how many numbers there are: 150 ÷ 5.",
                "Average = 30.",
            ],
        },
        {
            "question": "What is the simple interest on 2000 rupees at 5% per year for 3 years?",
            "options": ["250", "300", "350", "400"],
            "answer": "300",
            "steps": [
                "Simple interest = Principal × Rate × Time ÷ 100.",
                "= 2000 × 5 × 3 ÷ 100.",
                "= 30000 ÷ 100 = 300.",
            ],
        },
    ],
    "Logical Reasoning": [
        {
            "question": "What comes next? 2, 4, 8, 16, ?",
            "options": ["24", "30", "32", "36"],
            "answer": "32",
            "steps": [
                "Look at how each number changes: 2 to 4, 4 to 8, 8 to 16.",
                "Each number is multiplied by 2.",
                "So the next number is 16 × 2 = 32.",
            ],
        },
        {
            "question": "What comes next? 3, 6, 9, 12, ?",
            "options": ["14", "15", "16", "18"],
            "answer": "15",
            "steps": [
                "Find the gap between numbers: 6 − 3 = 3, 9 − 6 = 3, 12 − 9 = 3.",
                "The series adds 3 each time.",
                "So the next number is 12 + 3 = 15.",
            ],
        },
        {
            "question": "Which is the odd one out? Apple, Banana, Carrot, Mango",
            "options": ["Apple", "Banana", "Carrot", "Mango"],
            "answer": "Carrot",
            "steps": [
                "Group the items: Apple, Banana, and Mango are fruits.",
                "Carrot is a vegetable.",
                "So Carrot does not belong to the group.",
            ],
        },
        {
            "question": "If CAT is coded as DBU, how is DOG coded?",
            "options": ["EPH", "EPG", "DPH", "FPI"],
            "answer": "EPH",
            "steps": [
                "Compare CAT and DBU: C to D, A to B, T to U.",
                "Each letter moves one step forward in the alphabet.",
                "Apply the same rule: D to E, O to P, G to H.",
                "So DOG is coded as EPH.",
            ],
        },
        {
            "question": "A person walks 5 km north and then 5 km south. How far is the person from the starting point?",
            "options": ["0 km", "5 km", "10 km", "2.5 km"],
            "answer": "0 km",
            "steps": [
                "North and south are opposite directions.",
                "Walking 5 km north and then 5 km south cancels out.",
                "The person is back at the starting point, so the distance is 0 km.",
            ],
        },
        {
            "question": "Ravi is Sita's brother. Sita is Mohan's mother. How is Ravi related to Mohan?",
            "options": ["Father", "Maternal uncle", "Cousin", "Grandfather"],
            "answer": "Maternal uncle",
            "steps": [
                "Sita is Mohan's mother.",
                "Ravi is Sita's brother, so he is Mohan's mother's brother.",
                "A mother's brother is called a maternal uncle.",
            ],
        },
    ],
    "Verbal": [
        {
            "question": "Choose the synonym of 'Rapid'.",
            "options": ["Slow", "Quick", "Weak", "Late"],
            "answer": "Quick",
            "steps": [
                "A synonym is a word with a similar meaning.",
                "Rapid means moving at high speed.",
                "Quick has the same meaning. The other options are not similar.",
            ],
        },
        {
            "question": "Choose the antonym of 'Generous'.",
            "options": ["Kind", "Stingy", "Wealthy", "Polite"],
            "answer": "Stingy",
            "steps": [
                "An antonym is a word with the opposite meaning.",
                "Generous means willing to give freely.",
                "Stingy means unwilling to give, which is the opposite.",
            ],
        },
        {
            "question": "Fill in the blank: She ...... to college every day.",
            "options": ["go", "goes", "going", "gone"],
            "answer": "goes",
            "steps": [
                "The subject is 'She', which is third person singular.",
                "With he, she, or it in the present simple tense, the verb takes -s or -es.",
                "So the correct word is 'goes'.",
            ],
        },
        {
            "question": "Choose the correct sentence.",
            "options": ["He don't like tea.", "He doesn't like tea.", "He not like tea.", "He doesn't likes tea."],
            "answer": "He doesn't like tea.",
            "steps": [
                "With 'he', the correct helping verb is 'doesn't', not 'don't'.",
                "After 'doesn't', the main verb stays in its base form: 'like', not 'likes'.",
                "So 'He doesn't like tea.' is correct.",
            ],
        },
        {
            "question": "What does the idiom 'break the ice' mean?",
            "options": ["Start a conversation in a friendly way", "Break something frozen", "End a meeting", "Argue loudly"],
            "answer": "Start a conversation in a friendly way",
            "steps": [
                "An idiom has a meaning that is different from its individual words.",
                "'Break the ice' means to make people feel comfortable at the start of a meeting or conversation.",
                "So the answer is: start a conversation in a friendly way.",
            ],
        },
        {
            "question": "Choose the correctly spelled word.",
            "options": ["Recieve", "Receive", "Receeve", "Receve"],
            "answer": "Receive",
            "steps": [
                "Remember the rule: 'i' before 'e', except after 'c'.",
                "Here the letter before the pair is 'c', so the pair is spelled 'ei'.",
                "So the correct spelling is 'Receive'.",
            ],
        },
    ],
}

category = st.selectbox("Choose a topic", list(QUESTIONS.keys()))
questions = QUESTIONS[category]

answers = {}
for i, q in enumerate(questions):
    answers[i] = st.radio(
        f"Q{i + 1}. {q['question']}",
        q["options"],
        key=f"{category}_{i}",
        index=None,
    )

if st.button("Submit Answers"):
    score = 0
    st.subheader("Results")
    for i, q in enumerate(questions):
        selected = answers[i]
        if selected == q["answer"]:
            st.success(f"Q{i + 1}: Correct! ✅")
            score += 1
        else:
            st.error(f"Q{i + 1}: Incorrect ❌")
            st.write(f"Your answer: {selected if selected else 'No answer selected'}")
            st.write(f"Correct answer: {q['answer']}")
            st.write("**Step-by-step explanation:**")
            for step in q["steps"]:
                st.write(f"- {step}")
        st.write("---")

    st.subheader(f"Final Score: {score} / {len(questions)}")

    save_attempt("Aptitude", {
        "category": category,
        "score": score,
        "total": len(questions),
    })