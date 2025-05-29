import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="centered")

if 'running' not in st.session_state:
    st.session_state.running = False

def start():
    st.session_state.running = True

def stop():
    st.session_state.running = False
    st.experimental_rerun()

if not st.session_state.running:
    st.title("Training Word Announcer 🔊")

    with st.form("settings"):
        words_input = st.text_input("Enter words (comma-separated):", "Gun, Taser, Flashlight, Handcuffs, OC Spray, Baton")
        countdown_time = st.slider("Countdown seconds:", 1, 10, 3)
        start_button = st.form_submit_button("Start Training")

    if start_button:
        words = [w.strip() for w in words_input.split(",") if w.strip()]
        if not words:
            st.warning("Please enter at least one word.")
        else:
            st.session_state.words = words
            st.session_state.countdown = countdown_time
            start()

else:
    words_js_array = "[" + ",".join(f'"{w}"' for w in st.session_state.words) + "]"
    countdown = st.session_state.countdown

    # JS script runs training loop with countdown, word display, speech synthesis, fullscreen
    components.html(f"""
    <style>
        body {{
            margin: 0; padding: 0;
            height: 100vh; width: 100vw;
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
            background-color: #121212;
            color: #fff;
            font-family: Arial, sans-serif;
            user-select: none;
        }}
        h1 {{
            font-size: 6vw;
            margin: 0;
        }}
        button {{
            position: fixed;
            top: 20px;
            right: 20px;
            font-size: 1.5vw;
            padding: 0.5em 1em;
            cursor: pointer;
            border: none;
            border-radius: 5px;
            background: #e03e36;
            color: white;
            z-index: 9999;
        }}
    </style>

    <button id="stopBtn">⏹ Stop Training</button>

    <div id="display"><h1>Get Ready!</h1></div>

    <script>
    const words = {words_js_array};
    const countdownSeconds = {countdown};
    const display = document.getElementById('display');
    const stopBtn = document.getElementById('stopBtn');

    async function sleep(ms) {{
        return new Promise(resolve => setTimeout(resolve, ms));
    }}

    async function enterFullscreen() {{
        if (!document.fullscreenElement) {{
            await document.documentElement.requestFullscreen();
        }}
    }}

    async function exitFullscreen() {{
        if (document.fullscreenElement) {{
            await document.exitFullscreen();
        }}
    }}

    stopBtn.onclick = async () => {{
        await exitFullscreen();
        // Tell Streamlit to stop training by clicking the stop button on Streamlit side
        const streamlitStopBtn = window.parent.document.querySelector('button[kind="secondary"][title="Stop Training"],button[data-testid="stStopButton"]');
        if (streamlitStopBtn) {{
            streamlitStopBtn.click();
        }} else {{
            // fallback: reload page to reset
            window.parent.location.reload();
        }}
    }};

    async function trainingLoop() {{
        await enterFullscreen();
        while(true) {{
            // Countdown
            for(let i = countdownSeconds; i > 0; i--) {{
                display.innerHTML = `<h1>⏳ Get Ready: ${i}</h1>`;
                await sleep(1000);
            }}

            // Pick random word
            const word = words[Math.floor(Math.random() * words.length)];
            display.innerHTML = `<h1>🔊 ${word}</h1>`;

            // Speak the word
            let utterance = new SpeechSynthesisUtterance(word);
            utterance.lang = 'en-US';
            utterance.rate = 1.0;
            speechSynthesis.speak(utterance);

            // Wait for speech to finish + 1 second pause
            await new Promise(resolve => {{
                utterance.onend = () => setTimeout(resolve, 1000);
            }});
        }}
    }}

    trainingLoop();
    </script>
    """, height=500)

    if st.button("Stop Training"):
        stop()
