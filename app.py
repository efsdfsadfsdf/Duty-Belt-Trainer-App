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
        fullscreen = st.checkbox("Enable Fullscreen Mode", value=True)  # Default true for fullscreen effect
        start_training = st.form_submit_button("Start Training")

if start_training:
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
            #stopBtn {{
                position: fixed;
                bottom: 20px;
                right: 20px;
                background: #d9534f;
                border: none;
                padding: 15px 30px;
                font-size: 3vw;
                border-radius: 10px;
                color: white;
                cursor: pointer;
                user-select: none;
                z-index: 10;
                box-shadow: 0 4px 12px rgba(0,0,0,0.4);
                transition: background-color 0.3s ease;
            }}
            #stopBtn:hover {{
                background: #c9302c;
            }}
        </style>
        <div id="status">🔊 Training started...</div>
        <div id="countdown"></div>
        <div id="word"></div>
        <button id="stopBtn">⏹ Stop</button>

        <script>
            const words = {word_list_js};
            const minDelay = {min_delay} * 1000;
            const maxDelay = {max_delay} * 1000;
            const countdownTime = {countdown};

            let running = true;
            let speechSynthesisUtterance;

            {fullscreen_js}

            // Automatically request fullscreen on start if enabled
            {"toggleFullscreen();" if fullscreen else ""}

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

            const stopBtn = document.getElementById("stopBtn");
            const status = document.getElementById("status");

            stopBtn.onclick = () => {{
                running = false;
                speechSynthesis.cancel();
                status.textContent = "⏹ Training stopped.";
                document.getElementById("countdown").textContent = "";
                document.getElementById("word").textContent = "";
                if (document.fullscreenElement) {{
                    document.exitFullscreen();
                }}
            }};

            trainingLoop();
        </script>
        """, height=700)
