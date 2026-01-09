import streamlit as st

# 1. Page Configuration
st.set_page_config(page_title="Magical Spelling Bee", layout="wide")

# 2. Inject Tailwind & Custom CSS
st.markdown("""
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Spline+Sans:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
        /* Custom Theme Overrides */
        .stApp {
            background-color: #1a1022;
            color: white;
            font-family: 'Spline Sans', sans-serif;
        }
        
        /* Magical Gradient Card */
        .magical-banner {
            background: linear-gradient(135deg, #9d25f4 0%, #6d28d9 100%);
            border-radius: 20px;
            padding: 40px;
            text-align: center;
            border: 4px solid rgba(255,255,255,0.2);
            box-shadow: 0 0 40px rgba(157, 37, 244, 0.4);
            margin-bottom: 30px;
        }

        /* Quest & Daily Challenge Cards */
        .glass-card {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(157, 37, 244, 0.2);
            border-radius: 20px;
            padding: 25px;
        }

        /* Custom Buttons */
        .stButton>button {
            background: #9d25f4 !important;
            color: white !important;
            border-radius: 15px !important;
            border: none !important;
            width: 100%;
            font-weight: 900 !important;
            padding: 20px !important;
            box-shadow: 0 0 20px rgba(157, 37, 244, 0.4) !important;
        }
    </style>
""", unsafe_allow_html=True)

# 3. Header Area
col1, col2 = st.columns([1, 1])
with col1:
    st.markdown("<h2 style='color:#9d25f4; font-weight:900;'>✨ Magical Spelling</h2>", unsafe_allow_html=True)
with col2:
    st.markdown("<p style='text-align:right;'>Hana-chan 👤</p>", unsafe_allow_html=True)

# 4. Hero Banner
st.markdown("""
    <div class="magical-banner">
        <h1 style="font-size: 3rem; font-weight: 900; margin: 0;">GO FOR THE GOLD!</h1>
        <p style="font-style: italic; opacity: 0.9;">"Every word you master today is a step closer to the 2026 Trophy! ✨ 🏆 ✨"</p>
    </div>
""", unsafe_allow_html=True)

# 5. Main Content (Two Columns)
col_left, col_right = st.columns([1, 2], gap="large")

with col_left:
    st.markdown("""
        <div class="glass-card">
            <span style="background:#9d25f4; padding:5px 12px; border-radius:20px; font-size:12px;">LEVEL 15 SPELLCASTER</span>
            <h2 style="font-size:24px; font-weight:900; margin-top:15px;">Spelling Quest</h2>
            <p style="color:#ccc;">Master 5 new words today to unlock the Crystal Dictionary.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Using Streamlit's native progress bar for functionality
    st.write("Quest Progress: 60%")
    st.progress(0.6)

with col_right:
    with st.container(border=True):
        st.markdown("### 🪄 Daily Challenge")
        
        # Audio Player Simulation
        st.audio("http://www.w3schools.com/html/horse.ogg") 
        
        # User Input
        word_input = st.text_input("Type the word you hear:", placeholder="? ? ? ? ?", label_visibility="collapsed")
        
        if st.button("SUBMIT SPELLING"):
            st.balloons()
            st.success(f"Magical! You typed: {word_input}")

# 6. Word Collection Section
st.markdown("### ✨ Word List Collection")
word_cols = st.columns(4)

words = [
    {"name": "STARDUST", "lvl": "Level 4", "mastery": 0.8},
    {"name": "CELESTIAL", "lvl": "Level 5", "mastery": 0.2},
    {"name": "LUMINESCENCE", "lvl": "Level 7", "mastery": 0.05},
    {"name": "ETHEREAL", "lvl": "Level 6", "mastery": 1.0},
]

for i, word in enumerate(words):
    with word_cols[i]:
        st.markdown(f"""
            <div class="glass-card" style="text-align:center;">
                <div style="height:150px; background:#333; border-radius:10px; margin-bottom:10px; display:flex; align-items:center; justify-content:center;">
                    🖼️ Image
                </div>
                <h4 style="margin:0; font-weight:900;">{word['name']}</h4>
                <p style="color:#9d25f4; font-size:12px;">{word['lvl']}</p>
            </div>
        """, unsafe_allow_html=True)
        st.progress(word['mastery'])
