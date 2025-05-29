import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Duty Belt Trainer", layout="centered", initial_sidebar_state="collapsed")
st.title("🦺 Duty Belt Trainer")

if "running" not in st.session_state:
    st.session_state.running = False

def start_training():
    st.session_state.running = True

def stop_training():
    st.session_state.running = False

if not st.session_state.running:
    with st.form("settings_form"):
        words_input = st.text_input("Enter words (comma-separated):", "Gun, Taser, Flashlight, Handcuffs, OC Spray, Baton")
        min_delay = st.slider("Min delay (seconds)", 1, 10, 1)
        max_delay = st.slider("Max delay (seconds)", min_delay, 10, 4)
        countdown = st.slider("Countdown seconds before word", 1, 10, 3)
        fullscreen = st.checkbox("Enable Fullscreen Mode", value=True)
        start_training_btn = st.form_submit_button("Start Training", on_click=start_training)

    # Save inputs in session_state for use during training
    st.session_state.words_input = words_input
    st.session_state.min_delay = min_delay
    st.session_state.max_delay = max_delay
    st.session_state.countdown = countdown
    st.session_state.fullscreen = fullscreen

else:
    words = [w.strip() for w in st.session_state.words_input.split(",") if w.strip()]
    if not words:
        st.error("Please enter at least one word.")
    else:
        word_list_js = "[" + ", ".join([f'"{w}"' for w in words]) + "]"

        fullscreen_js = """
        function toggleFullscreen() {
            if (!document.fullscreenElement) {
                document.documentElement.requestFullscreen().catch((e) => console.log(e));
            }
        }
        """ if st.session_state.fullscreen else ""

        components.html(f"""
        <style>
            html, body {{
                margin: 0;
                padding: 0;
                height: 100%;
                background: #121212;
                color: #eee;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                overflow: hidden;
                user-select: none;
            }}
            #countdown {{
                font-size: 15vw;
                font-weight: 600;
                color: #ffa500;
                text-align: center;
                line-height: 1;
                margin: 0;
            }}
            #word {{
                font-size: 20vw;
                font-weight: 900;
                color: #00ffcc;
                text-align: center;
                line-height: 1;
                margin: 0;
                text-shadow: 0 0 30px #00ffcc;
            }}
            #status {{
                position: fixed;
                top: 10px;
                width: 100%;
                text-align: center;
                font-size: 2vw;
                color: #888;
                user-select: text;
            }}
        </style>
        <div id="status">🔊 Training started...</div>
        <div id="countdown"></div>
        <div id="word"></div>

        <script>
            const words = {word_list_js};
            const minDelay = {st.session_state.min_delay} * 1000;
            const maxDelay = {st.session_state.max_delay} * 1000;
            const countdownTime = {st.session_state.countdown};

            let running = true;
            let speechSynthesisUtterance;

            {fullscreen_js}

            // Request fullscreen if enabled
            {"toggleFullscreen();" if st.session_state.fullscreen else ""}

            function speakWord(text) {{
                speechSynthesis.cancel();
                speechSynthesisUtterance = new SpeechSynthesisUtterance(text);
                speechSynthesisUtterance.lang = 'en-US';
                speechSynthesisUtterance.rate = 1.0;
                speechSynthesis.speak(speechSynthesisUtterance);
            }}

            async function trainingLoop() {{
                while (running) {{
                    const delay = Math.random() * (maxDelay - minDelay) + minDelay;
                    await new Promise(r => setTimeout(r, delay));

                    for (let i = countdownTime; i > 0; i--) {{
                        if (!running) return;
                        document.getElementById("countdown").textContent = i;
                        document.getElementById("word").textContent = "";
                        await new Promise(r => setTimeout(r, 1000));
                    }}

                    if (!running) return;
                    const word = words[Math.floor(Math.random() * words.length)];
                    document.getElementById("countdown").textContent = "";
                    document.getElementById("word").textContent = word;
                    speakWord(word);
                }}
            }}

            trainingLoop();
        </script>
        """, height=700)

    # Streamlit stop button below the component to stop training and revert UI
    if st.button("⏹ Stop Training"):
        # Exit fullscreen via JS by injecting small component
        components.html("""
        <script>
        if (document.fullscreenElement) {
            document.exitFullscreen();
        }
        </script>
        """)
        st.session_state.running = False
        st.experimental_rerun()
