import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="centered")
st.title("Duty Belt Trainer 🔊 (iOS-Friendly Continuous Mode)")

# Input form
with st.form("trainer_form"):
    words_input = st.text_input("Words (comma-separated):", "Gun, Taser, Flashlight, Handcuffs, OC Spray, Baton")
    min_delay = st.slider("Minimum delay (seconds):", 1, 10, 1)
    max_delay = st.slider("Maximum delay (seconds):", min_delay, 10, 4)
    countdown_time = st.slider("Countdown before word (seconds):", 1, 10, 3)
    submitted = st.form_submit_button("Start Training")

if submitted:
    words = [w.strip() for w in words_input.split(",") if w.strip()]
    word_list = str(words).replace("'", '"')  # JSON-safe string for JS
    components.html(f"""
    <div style="text-align:center;font-size:24px;padding:20px;">
        <h3>👂 Training in progress...</h3>
        <div id="countdown">⏳</div>
        <div id="word" style="font-size:48px;margin-top:20px;"></div>
        <button onclick="stopTraining()" style="margin-top:30px;font-size:18px;padding:10px 20px;">⏹ Stop</button>
    </div>

    <script>
        const words = {word_list};
        const minDelay = {min_delay} * 1000;
        const maxDelay = {max_delay} * 1000;
        const countdownSeconds = {countdown_time};

        let running = true;

        function speak(text) {{
            const msg = new SpeechSynthesisUtterance(text);
            msg.lang = 'en-US';
            msg.rate = 1.0;
            window.speechSynthesis.cancel();
            window.speechSynthesis.speak(msg);
        }}

        function stopTraining() {{
            running = false;
        }}

        async function startLoop() {{
            while (running) {{
                const delay = Math.random() * (maxDelay - minDelay) + minDelay;
                await new Promise(res => setTimeout(res, delay));

                for (let i = countdownSeconds; i > 0; i--) {{
                    if (!running) return;
                    document.getElementById("countdown").innerText = "⏳ Get ready: " + i;
                    document.getElementById("word").innerText = "";
                    await new Promise(res => setTimeout(res, 1000));
                }}

                const word = words[Math.floor(Math.random() * words.length)];
                document.getElementById("countdown").innerText = "";
                document.getElementById("word").innerText = "🔊 " + word;
                speak(word);
            }}
        }}

        startLoop();
    </script>
    """, height=400)
