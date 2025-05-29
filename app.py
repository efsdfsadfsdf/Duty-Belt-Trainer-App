# save as app.py
import streamlit as st
import random
import time

st.set_page_config(layout="centered")

st.title("Training Word Announcer")

words_input = st.text_input("Enter words (comma-separated):", "Gun, Taser, Flashlight, Handcuffs, OC Spray, Baton")
countdown_time = st.slider("Countdown seconds:", 1, 10, 3)

if 'running' not in st.session_state:
    st.session_state.running = False

def reset_state():
    st.session_state.running = False

start = st.button("Start")
stop = st.button("Stop", on_click=reset_state)

if start:
    st.session_state.running = True

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

                # Show word
                word = random.choice(words)
                st.markdown(f"## 🔊 {word}")
                time.sleep(1)
