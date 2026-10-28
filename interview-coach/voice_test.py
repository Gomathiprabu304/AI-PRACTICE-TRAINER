import streamlit as st
from streamlit_mic_recorder import mic_recorder
import whisper
import language_tool_python
import tempfile
import os
from progress_tracker import save_attempt

st.title("AI-Powered LSRW Communication Coach")
st.write("Speaking Module — helping students build Listening, Speaking, Reading, and Writing confidence.")

@st.cache_resource
def load_whisper_model():
    return whisper.load_model("base")

@st.cache_resource
def load_grammar_tool():
    return language_tool_python.LanguageTool('en-US')

model = load_whisper_model()
tool = load_grammar_tool()

st.write("Click the mic, speak a few sentences, then click it again to stop.")

audio = mic_recorder(
    start_prompt="🎤 Start Recording",
    stop_prompt="⏹ Stop Recording",
    key="recorder"
)

if audio:
    st.audio(audio["bytes"])

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
    found_fillers = [word for word in filler_words if word in transcribed_text.lower()]

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
        "transcribed_text": transcribed_text,
        "filler_words_found": found_fillers,
        "grammar_issues": len(matches)
    })