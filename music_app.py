import streamlit as st
import numpy as np
from scipy.io import wavfile
import io

st.set_page_config(page_title="AI Music Generator", page_icon="🎵", layout="centered")

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
        color: #f8fafc;
    }
    .header-container {
        text-align: center;
        padding: 2rem 0rem;
        background: rgba(255, 255, 255, 0.03);
        border-radius: 16px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }
    .main-title {
        font-family: 'Poppins', sans-serif;
        font-size: 2.5rem !important;
        font-weight: 800 !important;
        background: linear-gradient(90deg, #38bdf8, #818cf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("""
    <div class="header-container">
        <h1 class="main-title">🎵 SYNTH MUSIC GENERATOR</h1>
        <p style="color: #94a3b8; font-size: 1.1rem;">Mathematical Audio Waveform Synthesis using NumPy & SciPy.</p>
    </div>
    """, unsafe_allow_html=True)

st.subheader("🎛️ Audio Synthesizer Controls")

wave_type = st.selectbox("Sound Profile / Theme", ["Ambient Poly-Chords (Smooth)", "Retro Arcade Lead (8-bit)", "Cyberpunk Ambient Echo"])
duration = st.slider("Duration (Seconds)", min_value=1, max_value=5, value=3)

if st.button("🎵 Generate & Synthesize Audio", type="primary", use_container_width=True):
    with st.spinner("Synthesizing multi-frequency audio..."):
        sample_rate = 44100
        t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
        
        # Isme hum alag-alag frequencies ko layer kar rahe hain chords banane ke liye
        if "Ambient" in wave_type:
            # Major Chord (C Major triad: 261.63, 329.63, 392.00 Hz) mixed together
            wave1 = np.sin(2 * np.pi * 261.63 * t)
            wave2 = np.sin(2 * np.pi * 329.63 * t)
            wave3 = np.sin(2 * np.pi * 392.00 * t)
            audio_data = (wave1 + wave2 + wave3) / 3
        elif "Retro" in wave_type:
            # 8-bit fast arpeggio sound using a square wave combined with harmony
            audio_data = np.sign(np.sin(2 * np.pi * 440 * t)) * 0.5 + np.sign(np.sin(2 * np.pi * 554.37 * t)) * 0.3
        else:
            # Deep sci-fi ambient sawtooth mix
            audio_data = (2 * (t * 110 - np.floor(t * 110 + 0.5))) * 0.6 + np.sin(2 * np.pi * 220 * t) * 0.4
            
        # Smooth fade-out effect taaki audio jhatke se band na ho
        fade_out = np.linspace(1.0, 0.0, len(t))
        audio_data = audio_data * fade_out
        
        audio_data = (audio_data * 32767 / np.max(np.abs(audio_data))).astype(np.int16)
        
        wav_buffer = io.BytesIO()
        wavfile.write(wav_buffer, sample_rate, audio_data)
        wav_bytes = wav_buffer.getvalue()
        
        st.write("")
        st.subheader("🎯 Play Synthesized Track")
        st.audio(wav_bytes, format="audio/wav")
        
        st.download_button(
            label="📥 Download Audio File",
            data=wav_bytes,
            file_name="synthesized_music.wav",
            mime="audio/wav",
            use_container_width=True
        )