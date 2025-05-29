# save as app.py
import streamlit as st
import random
import time
import streamlit.components.v1 as components

st.set_page_config(layout="centered")

st.title("Training Word Announcer 🔊")

# Input fields
words_input = st.text_input("Enter words (comma-separated):", "Gun, Taser, Flashlight, Handcuffs, OC Spray, Baton")
countdown_time = st.slider("Countdown seconds:", 1, 10, 3)

# Initialize session state
if 'running' not in st.session_state:
    st.session_state.running = False

# Stop function
def reset_state():
    st.session_state.running = False

# Buttons
start = st.button("Start")
stop = st.button("Stop", on_click=reset_state)

if start:
    st.session_state.running = True

# Main loop
if st.session_state.running:
    words = [w.strip() for w in words_input.split(",") if w.strip()]
    if not words:
        st.warning("Please enter at least one word.")
    else:
        with st.empty():
            while st.session_state.running:
                delay = random.uniform(1, 10)
                time.sleep(delay)

                # Countdown
                for i in range(countdown_time, 0, -1):
                    st.markdown(f"### ⏳ Get ready: {i}")
                    time.sleep(1)

                # Random word
                word = random.choice(words)

                # Use JavaScript to speak the word
                components.html(f"""
                    <script>
                        var msg = new SpeechSynthesisUtterance("{word}");
                        msg.lang = 'en-US';
                        msg.rate = 1.0;
                        window.speechSynthesis.speak(msg);
                    </script>
                    <h2 style='text-align: center;'>🔊 {word}</h2>
                """, height=100)

                time.sleep(1)
