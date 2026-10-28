import streamlit as st
from streamlit_mic_recorder import mic_recorder
import whisper
import language_tool_python
import numpy as np
import tempfile
import os
import re
from progress_tracker import save_attempt

st.title("AI-Powered LSRW Communication Coach")
st.subheader("Speaking Practice")

QUESTIONS = {
    "Visa interview": [
        {"q": "Why do you want to study in this country?",
         "tip": "Give two or three clear reasons, such as the course, the research, or the learning environment. Be specific and honest."},
        {"q": "Why did you choose this university and this course?",
         "tip": "Mention one or two things about the course or the university that match your interests and goals."},
        {"q": "Who is sponsoring your education, and how will you fund it?",
         "tip": "Answer directly and clearly. Say who is sponsoring you and how the costs will be covered."},
        {"q": "What are your plans after you finish your studies?",
         "tip": "Describe your career plan in simple, honest words and connect it to what you will study."},
        {"q": "How does this course connect to your bachelor's degree?",
         "tip": "Name your degree, then explain how the new course builds on it."},
    ],
    "University / admission interview": [
        {"q": "Tell me about yourself.",
         "tip": "Cover your education, your skills, and your goals in that order. Keep it under one minute."},
        {"q": "Describe a project you are proud of.",
         "tip": "Say what the project was, what you did yourself, and what you learned."},
        {"q": "What are your strengths and weaknesses?",
         "tip": "Pick one real strength with an example, and one weakness you are actively improving."},
    ],
    "Placement interview": [
        {"q": "Tell me about yourself.",
         "tip": "Start with your education, then your skills and projects, and finish with your career goal."},
        {"q": "Why should we hire you?",
         "tip": "Connect one or two of your skills to what the company needs."},
        {"q": "Where do you see yourself in five years?",
         "tip": "Show that you want to learn and grow, and keep your answer realistic."},
    ],
    "IELTS speaking": [
        {"q": "Describe a person who has influenced you.",
         "tip": "Say who they are, how you know them, and how they influenced you. Speak for about two minutes."},
        {"q": "Talk about a place you would like to visit.",
         "tip": "Say where it is, why you want to go, and what you would do there."},
    ],
}


@st.cache_resource
def load_whisper_model():
    return whisper.load_model("base")


@st.cache_resource
def load_grammar_tool():
    return language_tool_python.LanguageTool('en-US')


def analyze_audio(audio_bytes):
    """Measure background noise and voice level of a recording."""
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
            f.write(audio_bytes)
            path = f.name
        samples = whisper.load_audio(path)
        os.remove(path)
    except Exception:
        return None

    frame = 800  # 50 milliseconds at 16 kHz
    n = len(samples) // frame
    if n < 10:
        return None
    frames = samples[: n * frame].reshape(n, frame)
    rms = np.sqrt(np.mean(frames ** 2, axis=1)) + 1e-9
    db = 20 * np.log10(rms)
    noise_floor = float(np.percentile(db, 10))
    voice_level = float(np.percentile(db, 90))
    return {
        "noise_floor": noise_floor,
        "voice_level": voice_level,
        "clarity": voice_level - noise_floor,
    }


def get_labels(result):
    noise = result["noise_floor"]
    voice = result["voice_level"]
    if noise < -50:
        noise_label = "Low"
    elif noise < -40:
        noise_label = "Medium"
    else:
        noise_label = "High"
    if voice < -35:
        voice_label = "Too quiet"
    elif voice > -8:
        voice_label = "Too loud"
    else:
        voice_label = "Good"
    return noise_label, voice_label


def show_mic_check(result):
    if result is None:
        st.warning("The recording is too short. Please record about 4 seconds.")
        return
    noise_label, voice_label = get_labels(result)
    c1, c2, c3 = st.columns(3)
    c1.metric("Background noise", noise_label)
    c2.metric("Your voice", voice_label)
    c3.metric("Clarity", f"{result['clarity']:.0f} dB")

    if noise_label == "High":
        st.error("Your surroundings are noisy. Move to a quieter place or close the door, then check again.")
    elif voice_label == "Too quiet":
        st.warning("Your voice is too quiet. Move closer to the microphone or speak a little louder.")
    elif voice_label == "Too loud":
        st.warning("Your voice is too loud. Move a little away from the microphone.")
    elif result["clarity"] < 15:
        st.warning("Your voice is not much louder than the background. Try a quieter place.")
    else:
        st.success("Your microphone is ready. You can start your answer below.")


model = load_whisper_model()
tool = load_grammar_tool()

# ---------- Step 1: microphone check ----------
st.markdown("### Step 1: Check your microphone")
st.write("Click Start, stay quiet for 1 second, then say: *Hello, this is a mic test.* Then click Stop.")

mic_test = mic_recorder(
    start_prompt="🎤 Start mic check",
    stop_prompt="⏹ Stop mic check",
    key="mic_check"
)

if mic_test:
    show_mic_check(analyze_audio(mic_test["bytes"]))

st.divider()

# ---------- Step 2: practise ----------
st.markdown("### Step 2: Practise your answer")

category = st.selectbox("Choose a practice type", list(QUESTIONS.keys()))
question = st.selectbox("Choose a question", [item["q"] for item in QUESTIONS[category]])
tip = next(item["tip"] for item in QUESTIONS[category] if item["q"] == question)

st.info(f"**Question:** {question}")
with st.expander("Tip for answering"):
    st.write(tip)

st.write("Click the mic, speak your answer, then click it again to stop.")

audio = mic_recorder(
    start_prompt="🎤 Start Recording",
    stop_prompt="⏹ Stop Recording",
    key="recorder"
)

if audio:
    st.audio(audio["bytes"])

    quality = analyze_audio(audio["bytes"])
    if quality is not None:
        noise_label, voice_label = get_labels(quality)
        st.caption(f"Recording quality: background noise {noise_label}, voice {voice_label}.")
        if noise_label == "High":
            st.warning("There was a lot of background noise, so the transcription may have mistakes. Try again in a quieter place.")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
        tmp_file.write(audio["bytes"])
        tmp_path = tmp_file.name

    with st.spinner("Transcribing your speech..."):
        result = model.transcribe(tmp_path)
        transcribed_text = result["text"]

    os.remove(tmp_path)

    st.subheader("What you said:")
    st.write(transcribed_text)

    filler_words = ["um", "uh", "like", "you know", "actually", "basically", "so yeah"]
    found_fillers = [
        word for word in filler_words
        if re.search(r"\b" + re.escape(word) + r"\b", transcribed_text.lower())
    ]

    with st.spinner("Checking grammar..."):
        matches = tool.check(transcribed_text)

    st.subheader("Feedback:")

    if found_fillers:
        st.warning(f"Filler words detected: {', '.join(found_fillers)}")
    else:
        st.success("No filler words detected.")

    if len(matches) == 0:
        st.success("No grammar mistakes found!")
    else:
        st.write(f"Found {len(matches)} grammar issue(s):")
        for m in matches:
            st.write(f"❌ **Issue:** {m.message}")
            st.write(f"   → Suggestion: {', '.join(m.replacements) if m.replacements else 'No suggestion'}")
            st.write("---")

    save_attempt("Speaking", {
        "category": category,
        "question": question,
        "transcribed_text": transcribed_text,
        "filler_words_found": found_fillers,
        "grammar_issues": len(matches)
    })