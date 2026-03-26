# app.py
import streamlit as st
import sounddevice as sd
import numpy as np
import parselmouth
from parselmouth.praat import call
from scipy.io.wavfile import write
import random
import pandas as pd

# ===================== APP TITLE =====================
st.title("🧠 MindBuds - Your Digital Body Double")
st.write("Voice-based stress detection with empathetic interventions")
st.write("Check your stress and see it tracked over time!")

# ===================== STATE =====================
if "baseline" not in st.session_state:
    st.session_state.baseline = []
if "stress_history" not in st.session_state:
    st.session_state.stress_history = []

# ===================== AUDIO =====================
def record_audio(duration=5, fs=16000):
    st.info(f"🎤 Recording for {duration} seconds...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float32')
    sd.wait()
    return np.squeeze(audio)

# ===================== BIOMARKERS =====================
def extract_vocal_biomarkers(audio, sr=16000):
    write("temp.wav", sr, audio.astype(np.float32))
    sound = parselmouth.Sound("temp.wav")
    
    pitch = sound.to_pitch()
    pitch_values = pitch.selected_array['frequency']
    pitch_values = pitch_values[pitch_values > 0]
    
    jitter = 0.0
    shimmer = 0.0
    if len(pitch_values) > 10:
        point_process = call(sound, "To PointProcess (periodic, cc)", 75, 500)
        jitter = call(point_process, "Get jitter (local)", 0, 0, 0.0001, 0.02, 1.3)
        shimmer = call([sound, point_process], "Get shimmer (local)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    
    mean_pitch = float(np.mean(pitch_values)) if len(pitch_values) > 0 else 0.0
    pitch_std = float(np.std(pitch_values)) if len(pitch_values) > 0 else 0.0
    
    return {
        "mean_pitch_hz": round(mean_pitch, 1),
        "pitch_variability": round(pitch_std, 2),
        "jitter": round(jitter, 4),
        "shimmer": round(shimmer, 4),
    }

# ===================== BASELINE =====================
def update_baseline(biomarkers):
    st.session_state.baseline.append(biomarkers)
    if len(st.session_state.baseline) > 5:
        st.session_state.baseline.pop(0)

def get_relative_stress(biomarkers):
    if not st.session_state.baseline:
        return 50
    avg_pitch = sum(b["mean_pitch_hz"] for b in st.session_state.baseline) / len(st.session_state.baseline)
    avg_jitter = sum(b["jitter"] for b in st.session_state.baseline) / len(st.session_state.baseline)
    avg_shimmer = sum(b["shimmer"] for b in st.session_state.baseline) / len(st.session_state.baseline)
    
    pitch_diff = max(0, biomarkers["mean_pitch_hz"] - avg_pitch)
    jitter_diff = max(0, biomarkers["jitter"] - avg_jitter)
    shimmer_diff = max(0, biomarkers["shimmer"] - avg_shimmer)
    
    stress = int(0.3 * pitch_diff + 0.4 * jitter_diff * 100 + 0.3 * shimmer_diff * 100)
    return min(100, max(0, stress))

# ===================== SMOOTHING =====================
def smooth_stress(stress):
    st.session_state.stress_history.append(stress)
    if len(st.session_state.stress_history) > 20:  # keep last 20 readings
        st.session_state.stress_history.pop(0)
    return int(sum(st.session_state.stress_history) / len(st.session_state.stress_history))

# ===================== INTERVENTION =====================
def give_intervention(stress_level):
    interventions = {
        "low": ["You're doing great. Keep that steady flow.", "Nice calm energy today 👏"],
        "medium": ["Take a slow breath with me... In for 4, hold, out for 6.", 
                   "Your voice shows a bit of tension — let's reset."],
        "high": ["Hey, it's okay. You're safe. Let's do a quick box breath.", 
                 "I hear the stress. Pause for 30 seconds. You've got this."]
    }
    if stress_level < 40:
        return random.choice(interventions["low"])
    elif stress_level < 70:
        return random.choice(interventions["medium"])
    else:
        return random.choice(interventions["high"])

# ===================== APP INTERACTIONS =====================
st.header("Step 1: Record calm baseline")
st.write("Click below 3 times to record your calm baseline voice.")

if st.button("Record Baseline"):
    audio = record_audio(duration=6)
    biomarkers = extract_vocal_biomarkers(audio)
    update_baseline(biomarkers)
    st.success("Baseline recorded! Keep repeating until you have 3 readings.")
    st.write("Bioacoustic features:", biomarkers)

st.header("Step 2: Live Check-in")
if st.button("Start Check-in"):
    audio = record_audio(duration=6)
    biomarkers = extract_vocal_biomarkers(audio)
    raw_stress = get_relative_stress(biomarkers)
    smoothed_stress = smooth_stress(raw_stress)
    
    st.metric("Stress Level", f"{smoothed_stress}% (raw: {raw_stress}%)")
    st.write("Bioacoustic Analysis:", biomarkers)
    
    whisper = give_intervention(smoothed_stress)
    if smoothed_stress < 40:
        st.success(whisper)
    elif smoothed_stress < 70:
        st.warning(whisper)
    else:
        st.error(whisper)
    
    # --------- STRESS GRAPH ---------
    st.subheader("📈 Stress Level Over Time")
    df = pd.DataFrame({
        "Check-in": list(range(1, len(st.session_state.stress_history)+1)),
        "Stress Level (%)": st.session_state.stress_history
    })
    st.line_chart(df.set_index("Check-in"))