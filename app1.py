import streamlit as st
import random
import pandas as pd
from datetime import datetime

# =========================
# Page Config
# =========================
st.set_page_config(
    page_title="MindBuds – Stress Companion",
    page_icon="🧠",
    layout="centered"
)

# =========================
# Custom CSS
# =========================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600&family=DM+Serif+Display&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    h1, h2, h3 {
        font-family: 'DM Serif Display', serif;
    }

    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        color: #f0f0f0;
    }

    .block-container {
        padding-top: 2.5rem;
        max-width: 720px;
    }

    .stat-card {
        background: rgba(255,255,255,0.07);
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 16px;
        padding: 20px 24px;
        margin-bottom: 16px;
        backdrop-filter: blur(10px);
    }

    .stress-badge {
        font-size: 3rem;
        font-weight: 700;
        letter-spacing: -1px;
    }

    .tip-box {
        background: rgba(255,255,255,0.05);
        border-left: 3px solid #a78bfa;
        border-radius: 8px;
        padding: 14px 18px;
        margin-top: 12px;
        font-size: 0.93rem;
        color: #d1d5db;
    }

    .tag {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 0.78rem;
        font-weight: 600;
        margin-bottom: 8px;
    }
    .tag-low    { background: #065f46; color: #6ee7b7; }
    .tag-medium { background: #78350f; color: #fcd34d; }
    .tag-high   { background: #7f1d1d; color: #fca5a5; }

    div[data-testid="stMetricValue"] {
        font-size: 2.5rem !important;
        font-weight: 700;
        color: #a78bfa;
    }
    div[data-testid="stMetricLabel"] {
        font-size: 0.85rem;
        color: #9ca3af;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .stButton > button {
        background: linear-gradient(135deg, #7c3aed, #4f46e5);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.65rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        width: 100%;
        transition: opacity 0.2s;
    }
    .stButton > button:hover {
        opacity: 0.85;
        color: white;
    }

    hr { border-color: rgba(255,255,255,0.08); }

    .footer {
        text-align: center;
        font-size: 0.78rem;
        color: #6b7280;
        margin-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# =========================
# Session State Init
# =========================
if "history" not in st.session_state:
    st.session_state.history = []  # list of dicts: {stress, time, label}

# =========================
# Helper Functions
# =========================
def stress_label(level: int) -> tuple[str, str, str]:
    """Returns (label, emoji, css_class)"""
    if level < 40:
        return "Calm", "😌", "tag-low"
    elif level < 70:
        return "Moderate", "⚠️", "tag-medium"
    else:
        return "High", "🚨", "tag-high"

INTERVENTIONS = {
    "Calm": [
        "Great state to tackle deep work or learning. Ride this wave! 🌊",
        "Use this clarity for strategic planning or studying. 📚",
        "Perfect time for a creative session or journaling. ✍️",
    ],
    "Moderate": [
        "Try the **4-7-8 breathing**: inhale 4s, hold 7s, exhale 8s. Repeat 3×.",
        "Step away from your screen for 5 minutes. A short walk resets your cortisol. 🚶",
        "Drink a glass of water slowly and deliberately. Hydration affects focus. 💧",
    ],
    "High": [
        "🧊 Splash cold water on your face — it activates the dive reflex and slows your heart rate.",
        "Ground yourself: name **5 things you see, 4 you feel, 3 you hear**. It works.",
        "Box breathing: **4s in → 4s hold → 4s out → 4s hold**. Do this for 2 minutes.",
    ],
}

# =========================
# Header
# =========================
st.markdown("## 🧠 MindBuds")
st.markdown(
    "<p style='color:#9ca3af; margin-top:-12px; margin-bottom:24px;'>"
    "Your intelligent stress companion · Demo Mode</p>",
    unsafe_allow_html=True,
)

# =========================
# Stats Row (if history exists)
# =========================
if st.session_state.history:
    levels = [h["stress"] for h in st.session_state.history]
    col1, col2, col3 = st.columns(3)
    col1.metric("Latest", f"{levels[-1]}%")
    col2.metric("Average", f"{sum(levels)//len(levels)}%")
    col3.metric("Peak", f"{max(levels)}%")
    st.markdown("---")

# =========================
# Check-in Button
# =========================
col_btn, col_reset = st.columns([3, 1])

with col_btn:
    check_in = st.button("🔍 Simulate Stress Check-in")

with col_reset:
    if st.button("Reset"):
        st.session_state.history = []
        st.rerun()

# =========================
# Simulate Check-in
# =========================
if check_in:
    stress = random.randint(10, 100)
    label, emoji, css_class = stress_label(stress)
    tip = random.choice(INTERVENTIONS[label])
    timestamp = datetime.now().strftime("%H:%M:%S")

    st.session_state.history.append({
        "stress": stress,
        "time": timestamp,
        "label": label,
    })

    # Result card
    st.markdown(f"""
    <div class="stat-card">
        <span class="tag {css_class}">{emoji} {label}</span>
        <div class="stress-badge">{stress}%</div>
        <div style="color:#9ca3af; font-size:0.82rem; margin-top:4px;">Check-in at {timestamp}</div>
        <div class="tip-box">💡 {tip}</div>
    </div>
    """, unsafe_allow_html=True)

# =========================
# Stress History Chart
# =========================
if len(st.session_state.history) > 1:
    st.markdown("### Stress Trend")

    df = pd.DataFrame(st.session_state.history)
    df.index = range(1, len(df) + 1)
    df.index.name = "Check-in #"

    # Color-coded scatter via st.line_chart (simple, Streamlit-native)
    chart_df = df[["stress"]].rename(columns={"stress": "Stress Level (%)"})
    st.line_chart(chart_df, use_container_width=True, height=220, color="#a78bfa")

    # Session summary
    levels = df["stress"].tolist()
    high_count = sum(1 for x in levels if x >= 70)
    calm_count = sum(1 for x in levels if x < 40)

    st.markdown(f"""
    <div class="stat-card" style="font-size:0.88rem; color:#d1d5db;">
        📊 <strong>Session Summary</strong><br><br>
        • <strong>{len(levels)}</strong> check-ins recorded &nbsp;|&nbsp;
        <strong>{calm_count}</strong> calm &nbsp;|&nbsp;
        <strong>{high_count}</strong> high-stress<br>
        • Trend: {"📈 Rising" if len(levels) >= 3 and levels[-1] > levels[-3] else "📉 Falling" if len(levels) >= 3 and levels[-1] < levels[-3] else "➡️ Stable"}
    </div>
    """, unsafe_allow_html=True)

# =========================
# Empty State
# =========================
if not st.session_state.history:
    st.markdown("""
    <div style="text-align:center; padding: 40px 0; color:#6b7280;">
        <div style="font-size:3rem;">🧘</div>
        <div style="margin-top:12px; font-size:0.95rem;">
            Press <strong style="color:#a78bfa;">Simulate Stress Check-in</strong> to begin your session.
        </div>
    </div>
    """, unsafe_allow_html=True)

# =========================
# Footer
# =========================
st.markdown(
    "<div class='footer'>MindBuds Demo · No audio data collected · "
    "Built for Med+Tech exploration 🩺</div>",
    unsafe_allow_html=True,
)
