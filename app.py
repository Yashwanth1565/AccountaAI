"""
==========================================================
AccountaAI
AI Meeting Intelligence Platform (Premium Colored UI)
==========================================================
"""

import os
import streamlit as st

from backend.pipeline import pipeline
from backend.rag import rag
from backend.reminder import start_scheduler

# ==========================
# SETUP
# ==========================

os.makedirs("uploads", exist_ok=True)

st.set_page_config(
    page_title="AccountaAI",
    page_icon="📋",
    layout="wide"
)

if "scheduler_started" not in st.session_state:
    start_scheduler()
    st.session_state.scheduler_started = True

if "analysis" not in st.session_state:
    st.session_state.analysis = None

if "transcript" not in st.session_state:
    st.session_state.transcript = ""

if "GEMINI_API_KEY" in st.secrets:
    os.environ["GEMINI_API_KEY"] = st.secrets["GEMINI_API_KEY"]
else:
    st.error("GEMINI_API_KEY is missing. Please configure it in Streamlit Secrets.")
    st.stop()
# ==========================
# PREMIUM COLOR SYSTEM UI
# ==========================

st.markdown("""
<style>

/* BACKGROUND (MODERN GRADIENT LIKE STRIPE + OPENAI) */
.stApp {
    background: radial-gradient(circle at top, #0b1220, #050814 40%, #020409 100%);
    color: white;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a, #0b1220);
    border-right: 1px solid rgba(255,255,255,0.06);
}

/* HERO TITLE */
.title {
    font-size: 38px;
    font-weight: 900;
    background: linear-gradient(90deg, #38bdf8, #a78bfa, #22d3ee);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.subtitle {
    color: #94a3b8;
    margin-bottom: 20px;
    font-size: 15px;
}

/* GLASS CARDS (MODERN SaaS LOOK) */
.card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    padding: 14px;
    border-radius: 14px;
    margin-bottom: 10px;
    backdrop-filter: blur(10px);
    box-shadow: 0 10px 30px rgba(0,0,0,0.35);
}

/* BUTTONS (GRADIENT CTA STYLE) */
.stButton>button {
    width: 100%;
    background: linear-gradient(90deg, #3b82f6, #8b5cf6, #06b6d4);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 10px;
    font-weight: 700;
    box-shadow: 0 6px 20px rgba(59,130,246,0.25);
}

.stButton>button:hover {
    transform: scale(1.02);
    transition: 0.2s;
}

/* METRIC */
.metric-box {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 12px;
    padding: 10px;
}

</style>
""", unsafe_allow_html=True)

# ==========================
# SIDEBAR (CLEAN INFO ONLY)
# ==========================

with st.sidebar:

    st.markdown("## 📋 AccountaAI")

    st.caption("AI Meeting Intelligence System")

    st.divider()

    st.markdown("### 🧠 System Status")
    st.success("● Scheduler Active")
    st.info("● AI Pipeline Ready")

    st.divider()

    st.markdown("### ⚙ Stack")
    st.markdown("""
- Whisper STT  
- Gemini 2.5 Flash  
- ChromaDB  
- SQLite    
""")

    st.caption("v1.0 Production Build")

# ==========================
# HEADER
# ==========================

st.markdown('<div class="title">AccountaAI</div>', unsafe_allow_html=True)

st.markdown("""
<div class="subtitle">
Transform meeting conversations into Executable action plans.
</div>
""", unsafe_allow_html=True)

# ==========================
# UPLOAD + ACTION (CENTER FLOW)
# ==========================

st.markdown("## 📂 Upload Meeting")

uploaded_file = st.file_uploader(
    "Upload audio/video file",
    type=["mp3", "wav", "mp4", "m4a"]
)

audio_path = None
analyze = False

if uploaded_file:

    st.success(f"Uploaded: {uploaded_file.name}")

    audio_path = os.path.join("uploads", uploaded_file.name)

    with open(audio_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.info("Ready for AI analysis")

    analyze = st.button("🚀 Analyze Meeting")

# ==========================
# PIPELINE
# ==========================

if uploaded_file and analyze:

    progress = st.progress(0)
    status = st.empty()

    try:
        status.info("Extracting audio...")
        progress.progress(20)

        status.info("Transcribing...")
        progress.progress(40)

        status.info("AI analyzing...")
        progress.progress(70)

        result = pipeline.process(audio_path, uploaded_file.name)

        progress.progress(100)
        status.success("Analysis Completed")

        st.session_state.analysis = result["analysis"]
        st.session_state.transcript = result["transcript"]

    except Exception as e:
        st.error(str(e))

# ==========================
# RESULTS DASHBOARD (CLEAN + COLORED INSIGHTS)
# ==========================

if st.session_state.analysis:

    analysis = st.session_state.analysis

    st.divider()

    st.markdown("## 📄 Executive Summary")

    st.markdown(f"""
    <div class="card">
    {analysis.summary}
    </div>
    """, unsafe_allow_html=True)

    st.metric("⭐ Accountability Score", f"{analysis.accountability_score}/100")

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### ✅ Decisions")

        for d in analysis.decisions:
            st.markdown(f"""
            <div class="card" style="border-left: 4px solid #22c55e;">
            ✔ {d}
            </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown("### ⚠ Risks")

        for r in analysis.risks:
            st.markdown(f"""
            <div class="card" style="border-left: 4px solid #f59e0b;">
            ⚠ {r}
            </div>
            """, unsafe_allow_html=True)

    st.divider()

    st.markdown("### 📋 Action Items")

    if analysis.tasks:

        for t in analysis.tasks:
            st.markdown(f"""
            <div class="card" style="border-left: 4px solid #3b82f6;">
            <b>{t.task}</b><br>
            👤 {t.owner} | ⏰ {t.deadline} | 🔥 {t.priority} | 📌 {t.status}
            </div>
            """, unsafe_allow_html=True)

    st.divider()

    with st.expander("📜 Transcript"):
        st.write(st.session_state.transcript)

# ==========================
# MEMORY SEARCH
# ==========================

st.markdown("## 🧠 AI Memory")

q = st.text_input("Ask about past meetings")

if st.button("🔍 Search Memory"):

    if q.strip():
        with st.spinner("Searching..."):
            try:
                res = rag.ask(q)
                st.success(res)
            except Exception as e:
                st.error(str(e))
    else:
        st.warning("Enter a question")

# ==========================
# FOOTER
# ==========================

st.markdown("---")
st.caption("AccountaAI • AI Meeting Intelligence Platform")
