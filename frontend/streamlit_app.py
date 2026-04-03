import streamlit as st
import requests
import time

BASE_URL = "http://localhost:8000"

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="RegWatch AI — Compliance Intelligence",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;1,9..40,300&display=swap');

/* ── Base ─────────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.main .block-container {
    padding: 2rem 2.5rem 3rem 2.5rem;
    max-width: 1100px;
}

/* ── Hide default Streamlit chrome ─────────── */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ── Sidebar ──────────────────────────────── */
[data-testid="stSidebar"] {
    background: #0a0f1e;
    border-right: 1px solid #1e2a45;
}
[data-testid="stSidebar"] * {
    color: #c8d6f0 !important;
}
[data-testid="stSidebar"] .stMarkdown h1,
[data-testid="stSidebar"] .stMarkdown h2,
[data-testid="stSidebar"] .stMarkdown h3 {
    color: #e8f0ff !important;
    font-family: 'DM Serif Display', serif !important;
}

/* ── Main background ──────────────────────── */
.stApp {
    background: #f5f6fa;
}

/* ── Hero header ──────────────────────────── */
.hero-header {
    background: linear-gradient(135deg, #0a0f1e 0%, #0f1f40 50%, #0a1628 100%);
    border-radius: 16px;
    padding: 2.5rem 3rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero-header::before {
    content: '';
    position: absolute;
    top: -40px; right: -40px;
    width: 220px; height: 220px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(99,179,237,0.12) 0%, transparent 70%);
    pointer-events: none;
}
.hero-header::after {
    content: '';
    position: absolute;
    bottom: -60px; left: 30%;
    width: 300px; height: 180px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(66,153,225,0.07) 0%, transparent 70%);
    pointer-events: none;
}
.hero-eyebrow {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #63b3ed;
    margin-bottom: 0.6rem;
}
.hero-title {
    font-family: 'DM Serif Display', serif;
    font-size: 2.5rem;
    color: #e8f2ff;
    line-height: 1.15;
    margin: 0 0 0.75rem 0;
}
.hero-subtitle {
    font-size: 1rem;
    color: #8bafd6;
    font-weight: 300;
    max-width: 540px;
    line-height: 1.6;
}
.hero-badge {
    display: inline-block;
    background: rgba(99,179,237,0.15);
    border: 1px solid rgba(99,179,237,0.3);
    color: #90cdf4;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    padding: 0.25rem 0.75rem;
    border-radius: 999px;
    margin-top: 1rem;
}

/* ── Cards ────────────────────────────────── */
.card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 1.75rem 2rem;
    margin-bottom: 1.25rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05), 0 4px 16px rgba(0,0,0,0.04);
    transition: box-shadow 0.2s ease;
}
.card:hover {
    box-shadow: 0 2px 8px rgba(0,0,0,0.08), 0 8px 24px rgba(0,0,0,0.06);
}
.card-title {
    font-family: 'DM Serif Display', serif;
    font-size: 1.2rem;
    color: #0a0f1e;
    margin-bottom: 0.25rem;
}
.card-subtitle {
    font-size: 0.8rem;
    color: #718096;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 1rem;
}

/* ── Section labels ───────────────────────── */
.section-label {
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #4a5568;
    margin-bottom: 0.75rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: #e2e8f0;
}

/* ── Obligation pill ──────────────────────── */
.obligation-item {
    background: #f0f7ff;
    border-left: 3px solid #3182ce;
    border-radius: 0 8px 8px 0;
    padding: 0.65rem 1rem;
    margin-bottom: 0.5rem;
    font-size: 0.9rem;
    color: #2d3748;
    line-height: 1.5;
}
.rule-item {
    background: #f0fff4;
    border-left: 3px solid #38a169;
    border-radius: 0 8px 8px 0;
    padding: 0.65rem 1rem;
    margin-bottom: 0.5rem;
    font-size: 0.9rem;
    color: #2d3748;
    line-height: 1.5;
}

/* ── Risk badges ──────────────────────────── */
.risk-card {
    background: #fff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 0.75rem;
}
.risk-high {
    border-left: 4px solid #e53e3e;
}
.risk-medium {
    border-left: 4px solid #dd6b20;
}
.risk-low {
    border-left: 4px solid #38a169;
}
.risk-badge {
    display: inline-block;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    padding: 0.2rem 0.65rem;
    border-radius: 999px;
    margin-left: 0.5rem;
}
.risk-badge-high { background: #fff5f5; color: #c53030; border: 1px solid #fed7d7; }
.risk-badge-medium { background: #fffaf0; color: #c05621; border: 1px solid #fbd38d; }
.risk-badge-low { background: #f0fff4; color: #276749; border: 1px solid #c6f6d5; }
.risk-title {
    font-weight: 600;
    color: #1a202c;
    font-size: 0.95rem;
    margin-bottom: 0.4rem;
}
.risk-description {
    color: #4a5568;
    font-size: 0.875rem;
    line-height: 1.6;
}

/* ── Chat bubbles ─────────────────────────── */
.chat-user {
    background: #0f1f40;
    color: #e8f2ff;
    border-radius: 16px 16px 4px 16px;
    padding: 0.9rem 1.2rem;
    margin-bottom: 0.35rem;
    font-size: 0.9rem;
    line-height: 1.6;
    max-width: 85%;
    margin-left: auto;
}
.chat-user-label {
    text-align: right;
    font-size: 0.72rem;
    color: #718096;
    font-weight: 600;
    margin-bottom: 0.25rem;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}
.chat-ai {
    background: #fff;
    border: 1px solid #e2e8f0;
    color: #1a202c;
    border-radius: 16px 16px 16px 4px;
    padding: 0.9rem 1.2rem;
    margin-bottom: 0.35rem;
    font-size: 0.9rem;
    line-height: 1.6;
    max-width: 92%;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}
.chat-ai-label {
    font-size: 0.72rem;
    color: #3182ce;
    font-weight: 700;
    margin-bottom: 0.25rem;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}
.chat-key-point {
    background: #f7faff;
    border-left: 2px solid #90cdf4;
    padding: 0.4rem 0.75rem;
    margin: 0.3rem 0;
    border-radius: 0 6px 6px 0;
    font-size: 0.84rem;
    color: #2d3748;
}

/* ── Stat boxes ───────────────────────────── */
.stat-row {
    display: flex;
    gap: 1rem;
    margin-bottom: 1.5rem;
}
.stat-box {
    flex: 1;
    background: #fff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 1.1rem 1.25rem;
    text-align: center;
}
.stat-number {
    font-family: 'DM Serif Display', serif;
    font-size: 1.9rem;
    color: #0a0f1e;
    line-height: 1;
}
.stat-label {
    font-size: 0.75rem;
    color: #718096;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 0.3rem;
}

/* ── Status pill ──────────────────────────── */
.status-active {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: #f0fff4;
    border: 1px solid #c6f6d5;
    color: #276749;
    font-size: 0.75rem;
    font-weight: 600;
    padding: 0.3rem 0.8rem;
    border-radius: 999px;
}
.status-dot {
    width: 6px;
    height: 6px;
    background: #38a169;
    border-radius: 50%;
    display: inline-block;
}
.status-idle {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: #f7fafc;
    border: 1px solid #e2e8f0;
    color: #718096;
    font-size: 0.75rem;
    font-weight: 600;
    padding: 0.3rem 0.8rem;
    border-radius: 999px;
}

/* ── Upload zone ──────────────────────────── */
[data-testid="stFileUploader"] {
    border: 2px dashed #bee3f8 !important;
    border-radius: 12px !important;
    padding: 0.5rem !important;
    background: #f0f7ff !important;
    transition: border-color 0.2s ease;
}
[data-testid="stFileUploader"]:hover {
    border-color: #3182ce !important;
}

/* ── Buttons ──────────────────────────────── */
.stButton > button {
    background: #0f1f40 !important;
    color: #e8f2ff !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.875rem !important;
    padding: 0.55rem 1.5rem !important;
    transition: all 0.2s ease !important;
    letter-spacing: 0.02em !important;
}
.stButton > button:hover {
    background: #1a3260 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(15,31,64,0.25) !important;
}

/* ── Text input ───────────────────────────── */
.stTextInput > div > input {
    border-radius: 8px !important;
    border: 1.5px solid #e2e8f0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.9rem !important;
    padding: 0.6rem 1rem !important;
    transition: border-color 0.2s ease !important;
}
.stTextInput > div > input:focus {
    border-color: #3182ce !important;
    box-shadow: 0 0 0 3px rgba(49,130,206,0.12) !important;
}

/* ── Divider ──────────────────────────────── */
hr {
    border: none !important;
    border-top: 1px solid #e2e8f0 !important;
    margin: 1.5rem 0 !important;
}

/* ── Spinner ──────────────────────────────── */
.stSpinner > div {
    border-color: #3182ce transparent transparent transparent !important;
}

/* ── Expander ─────────────────────────────── */
[data-testid="stExpander"] {
    border: 1px solid #e2e8f0 !important;
    border-radius: 10px !important;
    background: #fff !important;
}

/* ── Success / Error / Warning ────────────── */
.stSuccess {
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stError {
    border-radius: 10px !important;
}

/* ── Sidebar nav items ────────────────────── */
.nav-item {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 8px;
    padding: 0.6rem 1rem;
    margin-bottom: 0.4rem;
    font-size: 0.875rem;
    color: #a0b8d8;
    cursor: pointer;
    transition: all 0.15s ease;
}
.nav-item:hover {
    background: rgba(255,255,255,0.1);
    color: #e8f2ff;
}
.nav-item-active {
    background: rgba(99,179,237,0.15) !important;
    border-color: rgba(99,179,237,0.3) !important;
    color: #90cdf4 !important;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────
defaults = {
    "filename": None,
    "analysis": None,
    "comparison": None,
    "chat_history": [],
    "compliance_risks": None,
    "active_tab": "upload",
    "docs_processed": 0,
    "total_obligations": 0,
    "total_rules": 0,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding: 0.5rem 0 1.5rem 0;'>
      <div style='font-family:"DM Serif Display",serif; font-size:1.4rem; color:#e8f2ff; line-height:1.2;'>
        ⚖️ RegWatch
      </div>
      <div style='font-size:0.72rem; color:#4a6fa5; font-weight:500; letter-spacing:0.12em; text-transform:uppercase; margin-top:0.25rem;'>
        AI Compliance Intelligence
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Navigation
    st.markdown("<div style='font-size:0.68rem;font-weight:700;letter-spacing:0.14em;text-transform:uppercase;color:#4a6fa5;margin-bottom:0.6rem;'>Navigation</div>", unsafe_allow_html=True)

    tabs = {
        "upload": ("📄", "Document Upload"),
        "analysis": ("🔍", "Document Analysis"),
        "risks": ("⚠️", "Compliance Risks"),
        "chat": ("💬", "Ask RegWatch AI"),
    }

    for key, (icon, label) in tabs.items():
        is_active = st.session_state.active_tab == key
        style_class = "nav-item nav-item-active" if is_active else "nav-item"
        if st.button(f"{icon}  {label}", key=f"nav_{key}", use_container_width=True):
            st.session_state.active_tab = key
            st.rerun()

    st.markdown("---")

    # Stats
    st.markdown("<div style='font-size:0.68rem;font-weight:700;letter-spacing:0.14em;text-transform:uppercase;color:#4a6fa5;margin-bottom:0.75rem;'>Session Stats</div>", unsafe_allow_html=True)

    st.markdown(f"""
    <div style='display:flex;flex-direction:column;gap:0.4rem;'>
      <div style='display:flex;justify-content:space-between;align-items:center;padding:0.5rem 0.75rem;background:rgba(255,255,255,0.04);border-radius:8px;'>
        <span style='font-size:0.8rem;color:#8bafd6;'>Documents</span>
        <span style='font-size:0.9rem;font-weight:700;color:#e8f2ff;'>{st.session_state.docs_processed}</span>
      </div>
      <div style='display:flex;justify-content:space-between;align-items:center;padding:0.5rem 0.75rem;background:rgba(255,255,255,0.04);border-radius:8px;'>
        <span style='font-size:0.8rem;color:#8bafd6;'>Obligations</span>
        <span style='font-size:0.9rem;font-weight:700;color:#e8f2ff;'>{st.session_state.total_obligations}</span>
      </div>
      <div style='display:flex;justify-content:space-between;align-items:center;padding:0.5rem 0.75rem;background:rgba(255,255,255,0.04);border-radius:8px;'>
        <span style='font-size:0.8rem;color:#8bafd6;'>Chat Messages</span>
        <span style='font-size:0.9rem;font-weight:700;color:#e8f2ff;'>{len(st.session_state.chat_history)}</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Status indicator
    if st.session_state.filename:
        st.markdown(f"""
        <div class='status-active'>
          <span class='status-dot'></span>
          Document loaded
        </div>
        <div style='font-size:0.78rem;color:#5a7fa5;margin-top:0.4rem;padding-left:0.25rem;'>
          📎 {st.session_state.filename}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class='status-idle'>
          No document loaded
        </div>
        """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# HERO HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class='hero-header'>
  <div class='hero-eyebrow'>Capital Markets · Regulatory Intelligence</div>
  <h1 class='hero-title'>AI-Powered Compliance<br>Assistant</h1>
  <p class='hero-subtitle'>
    Upload regulatory documents, extract obligations, identify compliance risks,
    and get real-time answers to your compliance queries — all in one place.
  </p>
  <div>
    <span class='hero-badge'>⚡ RAG-Powered</span>
    <span class='hero-badge' style='margin-left:0.5rem;'>🔍 Vector Search</span>
    <span class='hero-badge' style='margin-left:0.5rem;'>🛡️ Risk Analysis</span>
  </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# ACTIVE TAB CONTENT
# ─────────────────────────────────────────────
tab = st.session_state.active_tab


# ══════════════════════════════════════════════
#   TAB 1 — DOCUMENT UPLOAD
# ══════════════════════════════════════════════
if tab == "upload":

    st.markdown("<div class='section-label'>Document Ingestion</div>", unsafe_allow_html=True)

    col_upload, col_info = st.columns([3, 2], gap="large")

    with col_upload:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='card-subtitle'>Upload Regulatory Document</div>", unsafe_allow_html=True)
        st.markdown("<div class='card-title'>Select a PDF or TXT File</div>", unsafe_allow_html=True)

        uploaded_file = st.file_uploader(
            "Drop your regulatory document here",
            type=["pdf", "txt"],
            label_visibility="collapsed"
        )

        if uploaded_file is not None and st.session_state.filename != uploaded_file.name:
            st.session_state.filename = uploaded_file.name
            files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}

            with st.spinner("🔄 Ingesting document into vector database..."):
                try:
                    res = requests.post(f"{BASE_URL}/upload", files=files, timeout=120)
                    if res.status_code == 200:
                        data = res.json()
                        st.session_state.analysis = data["result"]["analysis"]
                        st.session_state.comparison = data["result"].get("comparison", {})
                        st.session_state.docs_processed += 1
                        obligs = st.session_state.analysis.get("obligations", [])
                        rules = st.session_state.analysis.get("rules", [])
                        st.session_state.total_obligations += len(obligs)
                        st.session_state.total_rules += len(rules)
                        st.success("✅ Document processed and indexed successfully!")

                        # Auto-navigate to analysis
                        time.sleep(0.5)
                        st.session_state.active_tab = "analysis"
                        st.rerun()
                    else:
                        st.error(f"❌ Upload failed (HTTP {res.status_code}). Is the backend running?")
                except requests.exceptions.ConnectionError:
                    st.error("❌ Cannot connect to backend. Please start the FastAPI server on port 8000.")

        st.markdown("</div>", unsafe_allow_html=True)

    with col_info:
        st.markdown("""
        <div class='card'>
          <div class='card-subtitle'>Supported Formats</div>
          <div class='card-title'>What Can You Upload?</div>
          <div style='margin-top:1rem;'>
            <div style='display:flex;align-items:flex-start;gap:0.75rem;margin-bottom:0.75rem;'>
              <div style='width:32px;height:32px;background:#fff5f5;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:1rem;flex-shrink:0;'>📕</div>
              <div>
                <div style='font-weight:600;font-size:0.875rem;color:#1a202c;'>PDF Documents</div>
                <div style='font-size:0.8rem;color:#718096;margin-top:0.15rem;'>SEC filings, compliance manuals, regulatory circulars</div>
              </div>
            </div>
            <div style='display:flex;align-items:flex-start;gap:0.75rem;margin-bottom:0.75rem;'>
              <div style='width:32px;height:32px;background:#f0f7ff;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:1rem;flex-shrink:0;'>📄</div>
              <div>
                <div style='font-weight:600;font-size:0.875rem;color:#1a202c;'>Plain Text Files</div>
                <div style='font-size:0.8rem;color:#718096;margin-top:0.15rem;'>Regulatory updates, policy documents, guidelines</div>
              </div>
            </div>
            <div style='display:flex;align-items:flex-start;gap:0.75rem;'>
              <div style='width:32px;height:32px;background:#f0fff4;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:1rem;flex-shrink:0;'>⚡</div>
              <div>
                <div style='font-weight:600;font-size:0.875rem;color:#1a202c;'>Auto-Vectorized</div>
                <div style='font-size:0.8rem;color:#718096;margin-top:0.15rem;'>Chunked and embedded into ChromaDB for semantic search</div>
              </div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    # Example use-cases
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='section-label'>Common Use Cases</div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    cases = [
        ("🏛️", "SEC & FINRA", "Upload SEC filings or FINRA compliance manuals to extract reporting requirements and penalties."),
        ("📊", "MiFID II", "Analyze MiFID II transaction reporting obligations and trade surveillance requirements."),
        ("🌐", "Basel III / IV", "Identify capital adequacy rules, liquidity coverage ratios, and leverage constraints."),
    ]
    for col, (icon, title, desc) in zip([col1, col2, col3], cases):
        with col:
            st.markdown(f"""
            <div class='card' style='text-align:center;'>
              <div style='font-size:2rem;margin-bottom:0.5rem;'>{icon}</div>
              <div style='font-weight:700;font-size:0.95rem;color:#0a0f1e;margin-bottom:0.5rem;'>{title}</div>
              <div style='font-size:0.82rem;color:#718096;line-height:1.55;'>{desc}</div>
            </div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════════════
#   TAB 2 — ANALYSIS
# ══════════════════════════════════════════════
elif tab == "analysis":

    if not st.session_state.analysis:
        st.markdown("""
        <div class='card' style='text-align:center;padding:3rem;'>
          <div style='font-size:3rem;margin-bottom:1rem;'>📂</div>
          <div style='font-family:"DM Serif Display",serif;font-size:1.4rem;color:#0a0f1e;margin-bottom:0.5rem;'>No Document Loaded</div>
          <div style='color:#718096;font-size:0.9rem;'>Upload a regulatory document first to see the analysis here.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("→ Go to Upload"):
            st.session_state.active_tab = "upload"
            st.rerun()
    else:
        analysis = st.session_state.analysis
        comparison = st.session_state.comparison or {}

        # Metrics row
        obligs = analysis.get("obligations", [])
        rules = analysis.get("rules", [])
        sims = comparison.get("similarities", [])
        diffs = comparison.get("differences", [])

        st.markdown(f"""
        <div class='stat-row'>
          <div class='stat-box'>
            <div class='stat-number'>{len(obligs)}</div>
            <div class='stat-label'>Obligations Found</div>
          </div>
          <div class='stat-box'>
            <div class='stat-number'>{len(rules)}</div>
            <div class='stat-label'>Rules Extracted</div>
          </div>
          <div class='stat-box'>
            <div class='stat-number'>{len(sims)}</div>
            <div class='stat-label'>Similarities</div>
          </div>
          <div class='stat-box'>
            <div class='stat-number'>{len(diffs)}</div>
            <div class='stat-label'>New Differences</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Summary card
        st.markdown("<div class='section-label'>Executive Summary</div>", unsafe_allow_html=True)
        summary = analysis.get("summary", "No summary available.")
        st.markdown(f"""
        <div class='card'>
          <div class='card-subtitle'>Document Overview</div>
          <div style='font-size:0.95rem;color:#2d3748;line-height:1.75;'>{summary}</div>
        </div>
        """, unsafe_allow_html=True)

        col_obl, col_rul = st.columns(2, gap="large")

        with col_obl:
            st.markdown("<div class='section-label'>Obligations</div>", unsafe_allow_html=True)
            if obligs:
                items_html = "".join([f"<div class='obligation-item'>{o}</div>" for o in obligs])
                st.markdown(f"<div class='card'><div class='card-subtitle'>Key Obligations</div>{items_html}</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='card'><div style='color:#718096;font-size:0.875rem;'>No obligations extracted.</div></div>", unsafe_allow_html=True)

        with col_rul:
            st.markdown("<div class='section-label'>Rules & Compliance</div>", unsafe_allow_html=True)
            if rules:
                items_html = "".join([f"<div class='rule-item'>{r}</div>" for r in rules])
                st.markdown(f"<div class='card'><div class='card-subtitle'>Identified Rules</div>{items_html}</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='card'><div style='color:#718096;font-size:0.875rem;'>No rules extracted.</div></div>", unsafe_allow_html=True)

        # Comparison
# ══════════════════════════════════════════════
#   TAB 3 — COMPLIANCE RISKS
# ══════════════════════════════════════════════
elif tab == "risks":

    st.markdown("<div class='section-label'>Risk Assessment</div>", unsafe_allow_html=True)

    if not st.session_state.filename:
        st.markdown("""
        <div class='card' style='text-align:center;padding:3rem;'>
          <div style='font-size:3rem;margin-bottom:1rem;'>⚠️</div>
          <div style='font-family:"DM Serif Display",serif;font-size:1.4rem;color:#0a0f1e;margin-bottom:0.5rem;'>No Document Loaded</div>
          <div style='color:#718096;font-size:0.9rem;'>Upload a document first to analyze compliance risks.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        col_btn, _ = st.columns([2, 3])
        with col_btn:
            run_analysis = st.button("⚡ Run Compliance Risk Analysis", use_container_width=True)

        if run_analysis:
            with st.spinner("🔍 Analyzing regulatory compliance risks..."):
                try:
                    res = requests.get(f"{BASE_URL}/compliance", timeout=120)
                    if res.status_code == 200:
                        st.session_state.compliance_risks = res.json().get("compliances", [])
                    else:
                        st.error("Failed to fetch compliance risks.")
                except requests.exceptions.ConnectionError:
                    st.error("❌ Cannot connect to backend.")

        if st.session_state.compliance_risks:
            risks = st.session_state.compliance_risks
            high = [r for r in risks if r.get("risk_level") == "High"]
            med  = [r for r in risks if r.get("risk_level") == "Medium"]
            low  = [r for r in risks if r.get("risk_level") == "Low"]

            # Risk summary strip
            st.markdown(f"""
            <div style='display:flex;gap:0.75rem;margin:1rem 0 1.5rem 0;'>
              <div style='flex:1;background:#fff5f5;border:1px solid #fed7d7;border-radius:10px;padding:0.9rem 1rem;text-align:center;'>
                <div style='font-family:"DM Serif Display",serif;font-size:1.7rem;color:#c53030;'>{len(high)}</div>
                <div style='font-size:0.72rem;font-weight:700;color:#e53e3e;text-transform:uppercase;letter-spacing:0.08em;'>High Risk</div>
              </div>
              <div style='flex:1;background:#fffaf0;border:1px solid #fbd38d;border-radius:10px;padding:0.9rem 1rem;text-align:center;'>
                <div style='font-family:"DM Serif Display",serif;font-size:1.7rem;color:#c05621;'>{len(med)}</div>
                <div style='font-size:0.72rem;font-weight:700;color:#dd6b20;text-transform:uppercase;letter-spacing:0.08em;'>Medium Risk</div>
              </div>
              <div style='flex:1;background:#f0fff4;border:1px solid #c6f6d5;border-radius:10px;padding:0.9rem 1rem;text-align:center;'>
                <div style='font-family:"DM Serif Display",serif;font-size:1.7rem;color:#276749;'>{len(low)}</div>
                <div style='font-size:0.72rem;font-weight:700;color:#38a169;text-transform:uppercase;letter-spacing:0.08em;'>Low Risk</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

            for item in risks:
                risk = item.get("risk_level", "Low")
                risk_class = {"High": "risk-high", "Medium": "risk-medium"}.get(risk, "risk-low")
                badge_class = {"High": "risk-badge-high", "Medium": "risk-badge-medium"}.get(risk, "risk-badge-low")

                st.markdown(f"""
                <div class='risk-card {risk_class}'>
                  <div style='display:flex;align-items:center;margin-bottom:0.5rem;'>
                    <div class='risk-title'>{item.get("title", "Untitled Risk")}</div>
                    <span class='risk-badge {badge_class}'>{risk}</span>
                  </div>
                  <div class='risk-description'>{item.get("description", "")}</div>
                </div>
                """, unsafe_allow_html=True)
        elif not run_analysis:
            st.markdown("""
            <div class='card' style='text-align:center;padding:2.5rem;background:#fafbff;'>
              <div style='font-size:2.5rem;margin-bottom:0.75rem;'>🛡️</div>
              <div style='font-size:0.95rem;color:#4a5568;'>Click the button above to run a full compliance risk analysis on your loaded documents.</div>
            </div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════════════
#   TAB 4 — CHAT
# ══════════════════════════════════════════════
elif tab == "chat":

    st.markdown("<div class='section-label'>Regulatory Q&A</div>", unsafe_allow_html=True)

    if not st.session_state.filename:
        st.markdown("""
        <div class='card' style='text-align:center;padding:3rem;'>
          <div style='font-size:3rem;margin-bottom:1rem;'>💬</div>
          <div style='font-family:"DM Serif Display",serif;font-size:1.4rem;color:#0a0f1e;margin-bottom:0.5rem;'>No Document Loaded</div>
          <div style='color:#718096;font-size:0.9rem;'>Upload a regulatory document to start asking questions.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Query input
        col_q, col_btn = st.columns([5, 1])
        with col_q:
            # Check for pending query from suggestion buttons
            pending = st.session_state.pop("_pending_query", "")
            query = st.text_input(
                "Ask a compliance question",
                value=pending,
                placeholder="e.g. What are the reporting deadlines for large transactions?",
                label_visibility="collapsed",
                key="chat_input"
            )
        with col_btn:
            ask_btn = st.button("Ask →", use_container_width=True)

        if ask_btn and query:
            with st.spinner("🤔 Searching regulatory knowledge base..."):
                try:
                    res = requests.post(
                        f"{BASE_URL}/ask",
                        json={"query": query, "filename": st.session_state.filename},
                        timeout=60
                    )
                    if res.status_code == 200:
                        data = res.json()
                        st.session_state.chat_history.append({
                            "q": query,
                            "a": data.get("answer", "No answer available."),
                            "points": data.get("key_points", [])
                        })
                        st.rerun()
                    else:
                        st.error("Failed to get an answer.")
                except requests.exceptions.ConnectionError:
                    st.error("❌ Cannot connect to backend.")

        # Chat history
        if st.session_state.chat_history:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<div class='section-label'>Conversation History</div>", unsafe_allow_html=True)

            for chat in reversed(st.session_state.chat_history):
                # User bubble
                st.markdown(f"""
                <div class='chat-user-label'>You</div>
                <div class='chat-user'>{chat['q']}</div>
                """, unsafe_allow_html=True)

                # AI bubble
                key_points_html = ""
                if chat["points"]:
                    kp_items = "".join([f"<div class='chat-key-point'>• {p}</div>" for p in chat["points"]])
                    key_points_html = f"<div style='margin-top:0.75rem;'><div style='font-size:0.72rem;font-weight:700;color:#3182ce;letter-spacing:0.08em;text-transform:uppercase;margin-bottom:0.35rem;'>Key Points</div>{kp_items}</div>"

                st.markdown(f"""
                <div class='chat-ai-label'>⚖️ RegWatch AI</div>
                <div class='chat-ai'>
                  {chat['a']}
                  {key_points_html}
                </div>
                <br>
                """, unsafe_allow_html=True)

            # Clear button
            col_clear, _ = st.columns([1, 4])
            with col_clear:
                if st.button("🗑️ Clear History"):
                    st.session_state.chat_history = []
                    st.rerun()
