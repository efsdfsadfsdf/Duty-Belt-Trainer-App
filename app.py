import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="centered")
st.title("Duty Belt Trainer 🔊 (iOS Continuous)")

with st.form("settings_form"):
    words_input = st.text_input("Words (comma-separated):", "Gun, Taser, Flashlight, Handcuffs, OC Spray, Baton")
    min_delay = st.slider("Min delay between words (seconds)", 1, 10, 1)
    max_delay = st.slider("Max delay between words (seconds)", min_delay, 10, 4)
    countdown = st.slider("Countdown before word (seconds)", 1, 10, 3)
    start = st.form_submit_button("Start Training")

if start:
    words = [w.strip() for w in words_input.split(",") if w.strip()]
    word_list = str(words).replace("'", '"')  # safe for JS

    components.html(f"""
    <div style="text-align: center; font-size: 24px; padding: 20px;">
        <button onclick="startTraining()" style="padding: 10px 20px; font-size: 20px;">▶️ Start Training</button>
        <div id="status" style="margin-top: 30px;"></div>
        <div id="countdown" style="font-size: 32px; color: gray;"></div>
        <div id="word" style="font-size: 48px; margin-top: 20px;"></div>
        <button onclick="stopTraining()" style="margin-top: 40px; font-size: 18px;">⏹ Stop</button>
    </div>

    <script>
        const words = {word_list};
        const minDelay = {min_delay} * 1000;
        const maxDelay = {max_delay} * 1000;
        const countdownTime = {countdown};

        let running = false;

        function speakWord(text) {{
            const msg = new SpeechSynthesisUtterance(text);
            msg.lang = 'en-US';
            msg.rate = 1.0;
            window.speechSynthesis.cancel();
            window.speechSynthesis.speak(msg);
        }}

        function stopTraining() {{
            running = false;
            document.getElementById("status").innerText = "⏹ Stopped";
        }}

        function startTraining() {{
            running = true;
            document.getElementById("status").innerText = "🔊 Training...";
            loop();
        }}

        async function loop() {{
            while (running) {{
                const delay = Math.rando
