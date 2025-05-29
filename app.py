import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Duty Belt Trainer", layout="centered", initial_sidebar_state="collapsed")
st.title("🦺 Duty Belt Trainer")

options_container = st.container()

with options_container:
    with st.form("settings_form"):
        words_input = st.text_input("Enter words (comma-separated):", "Gun, Taser, Flashlight, Handcuffs, OC Spray, Baton")
        min_delay = st.slider("Min delay (seconds)", 1, 10, 1)
        max_delay = st.slider("Max delay (seconds)", min_delay, 10, 4)
        countdown = st.slider("Countdown seconds before word", 1, 10, 3)
        fullscreen = st.checkbox("Enable Fullscreen Mode", value=False)
        start_training = st.form_submit_button("Start Training")

if start_training:
    # Hide the options form immediately
    options_container.empty()

    words = [w.strip() for w in words_input.split(",") if w.strip()]
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
        """ if fullscreen else ""

        components.html(f"""
        <style>
            body {{
                background: #121212;
                color: #eee;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 100vh;
                margin: 0;
            }}
            #countdown {{
                font-size: 3rem;
                margin-top: 1rem;
                color: #ffa500;
            }}
            #word {{
                font-size: 5rem;
                margin-top: 1rem;
                color: #00ffcc;
                font-weight: bold;
                text-shadow: 0 0 10px #00ffcc;
            }}
            button {{
                background: #0078d7;
                border: none;
                padding: 1rem 2rem;
                margin-top: 2rem;
                font-size: 1.5rem;
                border-radius: 8px;
                color: white;
                cursor: pointer;
                transition: background-color 0.3s ease;
            }}
            button:hover {{
                background: #005a9e;
            }}
        </style>
        <div>
            <!-- Hide start button by default because training already started -->
            <button id="startBtn" style="display:none;">▶️ Start Training</button>
            <button id="stopBtn">⏹ Stop</button>
            <div id="status" style="margin-top: 1rem; font-size: 1.5rem;">🔊 Training started...</div>
            <div id="countdown"></div>
            <div id="word"></div>
        </div>

        <script>
            const words = {word_list_js};
            const minDelay = {min_delay} * 1000;
            const maxDelay = {max_delay} * 1000;
            const countdownTime = {countdown};

            let running = true;
            let speechSynthesisUtterance;

            {fullscreen_js}

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
                        document.getElementById("countdown").textContent = "⏳ Get ready: " + i;
                        document.getElementById("word").textContent = "";
                        await new Promise(r => setTimeout(r, 1000));
                    }}

                    if (!running) return;
                    const word = words[Math.floor(Math.random() * words.length)];
                    document.getElementById("countdown").textContent = "";
                    document.getElementById("word").textContent = "🔊 " + word;
                    speakWord(word);
                }}
            }}

            const startBtn = document.getElementById("startBtn");
            const stopBtn = document.getElementById("stopBtn");
            const status = document.getElementById("status");

            stopBtn.onclick = () => {{
                running = false;
                speechSynthesis.cancel();
                status.textContent = "⏹ Training stopped.";
                startBtn.style.display = "inline-block";
                stopBtn.style.display = "none";
                document.getElementById("countdown").textContent = "";
                document.getElementById("word").textContent = "";
                if (document.fullscreenElement) {{
                    document.exitFullscreen();
                }}
            }};

            { "toggleFullscreen();" if fullscreen else "" }

            // Start the training loop immediately
            trainingLoop();
        </script>
        """, height=500)
