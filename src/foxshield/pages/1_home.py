import streamlit as st

# ── CUSTOM CSS FOR NAVY & CREAM THEME (FLAT DARK) ──
st.markdown("""
<style>
  /* Theme Tokens */
  :root {
    --bg-primary: #010736;   
    --bg-secondary: #0D1C42; 
    --accent: #22396F;       
    --text-primary: #FCF1D0; 
    --text-secondary: #8FA0C0;
    --card-bg: #0A1535;
  }

  /* Global App Background */
  .stApp {
      background-color: var(--bg-primary) !important;
      color: var(--text-primary) !important;
  }
  
  /* Sidebar Styling */
  [data-testid="stSidebar"] {
      background-color: var(--bg-secondary) !important;
      border-right: 1px solid var(--accent);
  }
  [data-testid="stSidebar"] * {
      color: var(--text-primary) !important;
  }
  
  /* Headings */
  h1, h2, h3, p, span, div {
      color: var(--text-primary) !important;
  }
  .sub, .stat-lbl, .footer {
      color: var(--text-secondary) !important;
  }
  
  /* Hero Section */
  .hero {
      background-color: var(--bg-secondary);
      border: 1px solid var(--accent);
      padding: 2.5rem;
      border-radius: 16px;
      margin-bottom: 2rem;
  }
  .hero-badge {
      display: inline-block;
      background: rgba(252, 241, 208, 0.1);
      border: 1px solid var(--accent);
      color: var(--text-primary);
      padding: 4px 12px;
      border-radius: 20px;
      font-size: 0.7rem;
      font-weight: 700;
      letter-spacing: 1px;
      text-transform: uppercase;
      margin-bottom: 1rem;
  }
  
  /* Stats Container */
  .stats-container {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 1rem;
      margin-bottom: 2.5rem;
  }
  .stat-box {
      background-color: var(--card-bg);
      border: 1px solid var(--accent);
      border-radius: 12px;
      padding: 1.5rem;
      text-align: center;
  }
  .stat-num {
      font-size: 1.8rem;
      font-weight: 800;
      color: var(--text-primary);
      margin-bottom: 0.5rem;
  }
  
  /* Feature Cards Grid */
  .feature-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 1.2rem;
      margin-bottom: 2.5rem;
  }
  .card {
      background-color: var(--card-bg);
      border: 1px solid var(--accent);
      border-radius: 12px;
      padding: 1.5rem;
      height: 100%;
  }
  .card-icon {
      font-size: 1.8rem;
      margin-bottom: 1rem;
      display: block;
  }
  
  /* Info Banner */
  .info-banner {
      background-color: rgba(34, 57, 111, 0.3);
      border-left: 4px solid var(--text-primary);
      padding: 1.2rem;
      border-radius: 8px;
      margin-top: 1rem;
      display: flex;
      align-items: center;
      gap: 1rem;
  }
  
  /* Primary Button Override (Flat Dark Style) */
  div[data-testid="stBaseButton-primary"] {
      background-color: var(--accent) !important;
      color: var(--text-primary) !important;
      border: 1px solid var(--text-primary) !important;
      border-radius: 8px !important;
      font-weight: 600 !important;
  }
  div[data-testid="stBaseButton-primary"]:hover {
      background-color: var(--text-primary) !important;
      color: var(--bg-primary) !important;
  }
  
  /* Footer */
  .footer {
      text-align: center;
      margin-top: 3rem;
      padding-top: 1rem;
      border-top: 1px solid var(--accent);
      font-size: 0.8rem;
  }
</style>
""", unsafe_allow_html=True)

# ── MAIN CONTENT WRAPPER ──
st.markdown('<div class="home-wrap">', unsafe_allow_html=True)

# ─ HERO SECTION ──
st.markdown("""
<div class="hero">
  <div class="hero-badge">Hackathon Round 3</div>
  <h1>🦊 FoxShield</h1>
  <p class="tagline" style="font-size: 1.2rem; font-weight: 600; margin: 0.5rem 0;">Context-Aware Privacy Leak Scanner for Government Portals</p>
  <p class="sub">Detects accidental PII exposure in PDFs and spreadsheets — while distinguishing legitimate transparency disclosures (RTI responses) from actual data leaks using an isolated Docker sandbox.</p>
</div>
""", unsafe_allow_html=True)

# ─ STATS STRIP ──
st.markdown("""
<div class="stats-container">
  <div class="stat-box">
    <div class="stat-num">12+</div>
    <div class="stat-lbl">PII Patterns</div>
  </div>
  <div class="stat-box">
    <div class="stat-num">RTI-Aware</div>
    <div class="stat-lbl">Context Engine</div>
  </div>
  <div class="stat-box">
    <div class="stat-num">Zero Egress</div>
    <div class="stat-lbl">Secure Sandbox</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─ HOW IT WORKS ──
st.markdown('<h2 style="margin-bottom: 1.5rem;">⚙️ How It Works</h2>', unsafe_allow_html=True)

st.markdown("""
<div class="feature-grid">
  <div class="card">
    <span class="card-icon">📄</span>
    <h3>1 · Upload Securely</h3>
    <p class="sub">Drop in a PDF or spreadsheet. Files are processed entirely in volatile RAM within an isolated container.</p>
  </div>
  <div class="card">
    <span class="card-icon">🧠</span>
    <h3>2 · Context Analysis</h3>
    <p class="sub">The engine scores each finding: distinguishing legitimate RTI disclosures from genuine confidential leaks.</p>
  </div>
  <div class="card">
    <span class="card-icon">🛡️</span>
    <h3>3 · Risk & Redact</h3>
    <p class="sub">View forensic risk quantification, estimated financial exposure, and preview redactions before export.</p>
  </div>
</div>
""", unsafe_allow_html=True)

# ─ BANNER + CTA ──
st.markdown("""
<div class="info-banner">
  <span style="font-size:1.5rem;">💡</span>
  <div>
    <strong>MVP Focus:</strong> Proving contextual distinction (RTI vs. Leak) inside a secure Docker sandbox with DPDP Act 2023 aligned financial risk quantification. No data ever leaves the container.
  </div>
</div>
""", unsafe_allow_html=True)

st.write("")
st.page_link("pages/2_scan.py", label="🔍 Launch Secure Scanner →")

# ─ FOOTER ──
st.markdown("""
<div class="footer">FoxShield · Team CryptoFox · Privacy-Aware Document Analysis</div>
</div>
""", unsafe_allow_html=True)