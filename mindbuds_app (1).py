import streamlit as st
import random
import pandas as pd
from datetime import datetime

# ─────────────────────────────────────────
# Page config  (must be FIRST st call)
# ─────────────────────────────────────────
st.set_page_config(
    page_title="MindBuds – Stress Companion",
    page_icon="🧠",
    layout="centered",
)

# ─────────────────────────────────────────
# Styling
# ─────────────────────────────────────────
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600&family=DM+Serif+Display&display=swap');

    html, body, [class*="css"]          { font-family: 'DM Sans', sans-serif; }
    h1, h2, h3                          { font-family: 'DM Serif Display', serif; }

    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        color: #f0f0f0;
    }
    .block-container { padding-top: 2.5rem; max-width: 720px; }

    .mb-card {
        background: rgba(255,255,255,0.07);
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 16px;
        padding: 20px 24px;
        margin-bottom: 16px;
    }
    .stress-number { font-size: 3rem; font-weight: 700; letter-spacing: -1px; }

    .tag {
        display: inline-block;
        padding: 3px 12px;
        border-radius: 20px;
        font-size: 0.78rem;
        font-weight: 600;
        margin-bottom: 8px;
    }
    .tag-low  { background:#065f46; color:#6ee7b7; }
    .tag-mid  { background:#78350f; color:#fcd34d; }
    .tag-high { background:#7f1d1d; color:#fca5a5; }

    .tip-box {
        background: rgba(255,255,255,0.05);
        border-left: 3px solid #a78bfa;
        border-radius: 8px;
        padding: 12px 16px;
        margin-top: 12px;
        font-size: 0.92rem;
        color: #d1d5db;
    }

    div[data-testid="stMetricValue"] { font-size: 2.2rem !important; color: #a78bfa; font-weight: 700; }
    div[data-testid="stMetricLabel"] { font-size: 0.78rem; color: #9ca3af; text-transform: uppercase; letter-spacing: .05em; }

    .stButton > button {
        background: linear-gradient(135deg, #7c3aed, #4f46e5);
        color: white !important;
        border: none;
        border-radius: 12px;
        padding: 0.65rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        width: 100%;
        transition: opacity .2s;
    }
    .stButton > button:hover { opacity: .85; }

    hr { border-color: rgba(255,255,255,0.08); }
    .footer { text-align:center; font-size:.78rem; color:#6b7280; margin-top:2rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────
# Session state
# ─────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []

# ─────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────
def get_level_info(score):
    if score < 40:
        return "Calm", "😌", "tag-low"
    elif score < 70:
        return "Moderate", "⚠️", "tag-mid"
    else:
        return "High", "🚨", "tag-high"


TIPS = {
    "Calm": [
        "Great state to tackle deep work or study. Ride this wave! 🌊",
        "Perfect time for strategic planning or writing. 📝",
        "Your cortisol is low – ideal for creative thinking. 💡",
    ],
    "Moderate": [
        "Try 4-7-8 breathing: inhale 4s · hold 7s · exhale 8s. Repeat 3x.",
        "Step away from your screen for 5 mins. A short walk resets cortisol. 🚶",
        "Drink a glass of water slowly. Hydration directly affects focus. 💧",
    ],
    "High": [
        "🧊 Splash cold water on your face – activates the dive reflex and slows heart rate.",
        "Ground yourself: name 5 things you see, 4 you feel, 3 you hear.",
        "Box breathing: 4s in → 4s hold → 4s out → 4s hold. Two minutes does it.",
    ],
}

# ─────────────────────────────────────────
# Header
# ─────────────────────────────────────────
st.markdown("## 🧠 MindBuds")
st.markdown(
    "<p style='color:#9ca3af;margin-top:-12px;margin-bottom:20px;'>"
    "Your intelligent stress companion &nbsp;·&nbsp; Demo Mode</p>",
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────
# Stats row
# ─────────────────────────────────────────
if st.session_state.history:
    scores = [h["stress"] for h in st.session_state.history]
    c1, c2, c3 = st.columns(3)
    c1.metric("Latest",  str(scores[-1]) + "%")
    c2.metric("Average", str(int(sum(scores) / len(scores))) + "%")
    c3.metric("Peak",    str(max(scores)) + "%")
    st.markdown("---")

# ─────────────────────────────────────────
# Buttons
# ─────────────────────────────────────────
btn_col, rst_col = st.columns([4, 1])
with btn_col:
    do_checkin = st.button("🔍  Simulate Stress Check-in")
with rst_col:
    if st.button("Reset"):
        st.session_state.history = []
        st.rerun()

# ─────────────────────────────────────────
# Check-in
# ─────────────────────────────────────────
if do_checkin:
    score = random.randint(10, 100)
    label, emoji, css_class = get_level_info(score)
    tip   = random.choice(TIPS[label])
    ts    = datetime.now().strftime("%H:%M:%S")

    st.session_state.history.append({"stress": score, "time": ts, "label": label})

    html_card = (
        '<div class="mb-card">'
        '<span class="tag ' + css_class + '">' + emoji + ' ' + label + '</span>'
        '<div class="stress-number">' + str(score) + '%</div>'
        '<div style="color:#9ca3af;font-size:.82rem;margin-top:4px;">Check-in at ' + ts + '</div>'
        '<div class="tip-box">💡 ' + tip + '</div>'
        '</div>'
    )
    st.markdown(html_card, unsafe_allow_html=True)

# ─────────────────────────────────────────
# Trend chart
# ─────────────────────────────────────────
if len(st.session_state.history) > 1:
    st.markdown("### Stress Trend")

    df = pd.DataFrame(st.session_state.history)
    df.index = range(1, len(df) + 1)
    df.index.name = "Check-in #"

    st.line_chart(
        df[["stress"]].rename(columns={"stress": "Stress Level (%)"}),
        use_container_width=True,
        height=220,
        color="#a78bfa",
    )

    scores = df["stress"].tolist()
    calm_n = sum(1 for x in scores if x < 40)
    high_n = sum(1 for x in scores if x >= 70)

    if len(scores) >= 3:
        if scores[-1] > scores[-3]:
            trend = "📈 Rising"
        elif scores[-1] < scores[-3]:
            trend = "📉 Falling"
        else:
            trend = "➡️ Stable"
    else:
        trend = "➡️ Too few check-ins to trend"

    summary_html = (
        '<div class="mb-card" style="font-size:.88rem;color:#d1d5db;">'
        '📊 <strong>Session Summary</strong><br><br>'
        '&bull; <strong>' + str(len(scores)) + '</strong> check-ins &nbsp;|&nbsp;'
        '<strong>' + str(calm_n) + '</strong> calm &nbsp;|&nbsp;'
        '<strong>' + str(high_n) + '</strong> high-stress<br>'
        '&bull; Trend: ' + trend +
        '</div>'
    )
    st.markdown(summary_html, unsafe_allow_html=True)

# ─────────────────────────────────────────
# Empty state
# ─────────────────────────────────────────
if not st.session_state.history:
    st.markdown(
        '<div style="text-align:center;padding:40px 0;color:#6b7280;">'
        '<div style="font-size:3rem;">🧘</div>'
        '<div style="margin-top:12px;font-size:.95rem;">'
        'Press <strong style="color:#a78bfa;">Simulate Stress Check-in</strong>'
        ' to begin your session.</div></div>',
        unsafe_allow_html=True,
    )

# ─────────────────────────────────────────
# Footer
# ─────────────────────────────────────────
st.markdown(
    "<div class='footer'>MindBuds Demo &nbsp;·&nbsp; No audio data collected"
    " &nbsp;·&nbsp; Built for Med+Tech exploration 🩺</div>",
    unsafe_allow_html=True,
)
