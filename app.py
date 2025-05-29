import streamlit as st
import streamlit.components.v1 as components

if 'running' not in st.session_state:
    st.session_state.running = False

def start():
    st.session_state.running = True

def stop():
    st.session_state.running = False
    st.experimental_rerun()

if not st.session_state.running:
    # Show options
    with st.form("settings"):
        words_input = st.text_input("Enter words", "Gun, Taser, Flashlight, Handcuffs, OC Spray, Baton")
        countdown = st.slider("Countdown seconds", 1, 10, 3)
        start_button = st.form_submit_button("Start Training")
    if start_button:
        st.session_state.words = [w.strip() for w in words_input.split(",") if w.strip()]
        st.session_state.countdown = countdown
        start()
else:
    # Show training UI + Stop button
    words_js_array = "[" + ",".join([f'"{w}"' for w in st.session_state.words]) + "]"
    components.html(f"""
    <script>
    const words = {words_js_array};
    const countdownSeconds = {st.session_state.countdown};

    function sleep(ms) {{
        return new Promise(resolve => setTimeout(resolve, ms));
    }}

    async function training() {{
        while (true) {{
            for (let i = countdownSeconds; i > 0; i--) {{
                document.body.innerHTML = `<h1>Get ready: {`{i}`}</h1>`;
                await sleep(1000);
            }}
            let word = words[Math.floor(Math.random() * words.length)];
            document.body.innerHTML = `<h1 style="color:green;">{word}</h1>`;
            // Speak word
            let utterance = new SpeechSynthesisUtterance(word);
            speechSynthesis.speak(utterance);
            await sleep(2000);
        }}
    }}

    training();
    </script>
    """, height=300)

    if st.button("Stop Training"):
        stop()
