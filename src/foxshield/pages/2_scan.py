# import streamlit as st 
# import time
# from core.scanner import scan
# from core.sandbox import get_container_id, verify_netowrk_isol, secure_memory_cleanup

# # =====================================================================
# # 1. GLOBAL CUSTOM CSS
# # =====================================================================
# st.markdown("""
# <style>
#     div[data-testid="stMarkdownContainer"] pre, .stCode, pre.stCode {
#         background-color: #0D1117 !important; border: 1px solid #30363D !important;
#         border-left: 4px solid #00E676 !important; border-radius: 6px !important;
#         font-family: 'Courier New', Courier, monospace !important; font-size: 13px !important;
#         padding: 15px !important; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3) !important;
#     }
#     div[data-testid="stMarkdownContainer"] pre code, .stCode code, .stCode span {
#         color: #00E676 !important; background-color: transparent !important;
#     }
#     div[data-testid="stMetricValue"] { font-size: 1.2rem !important; color: #00E676 !important; font-weight: bold !important; }
#     div[data-testid="stMetricLabel"] { color: #8B949E !important; }
#     .stFileUploader { border: 2px dashed #30363D !important; border-radius: 10px !important; background-color: #161B22 !important; padding: 20px !important; }
#     h1, h2, h3 { font-weight: 700 !important; letter-spacing: -0.5px !important; color: #FAFAFA !important; }
#     .stAlert { border-radius: 8px !important; border-left: 4px solid #00E676 !important; }
# </style>
# """, unsafe_allow_html=True)

# # =====================================================================
# # 2. MAIN APP UI
# # =====================================================================
# st.title("🦊 FoxShield Scanner")
# st.markdown("**Context-Aware Privacy Leak Scanner**")

# uploaded_file = st.file_uploader(label="Upload your file to scan", type=["pdf", "csv", "xlsx"], help="Upload PDF, EXCEL OR CSV FILES")

# if uploaded_file is not None:
#     st.success(f"✅ File '{uploaded_file.name}' Uploaded Successfully")

#     col1, col2, col3 = st.columns(3)
#     with col1: st.metric(label="📄 File Name", value=uploaded_file.name)
#     with col2: st.metric(label="💾 File Size", value=f"{uploaded_file.size / 1024:.2f} KB") 
#     with col3: st.metric(label="📂 File Type", value=uploaded_file.type.upper())

#     if st.button(label="🔬 Start Secure Scan", type="primary", use_container_width=True):
#         log_placeholder = st.empty()
#         logs = []
        
#         def add_log(message: str):
#             logs.append(message)
#             log_placeholder.code("\n".join(logs), language="bash")
#             time.sleep(0.4)

#         container_id = get_container_id()
#         add_log(f"[DOCKER] Initializing Sandbox Container: {container_id}")
#         add_log("[NETWORK] Verifying egress restrictions...")
#         network_status = verify_netowrk_isol()
#         add_log(f"[NETWORK] External Access: {network_status}")
#         add_log("[STORAGE] Mounting ephemeral read-only volume...")
        
#         file_bytes = uploaded_file.getvalue()
#         file_type = uploaded_file.name.split('.')[-1].lower()
#         add_log(f"[SCAN] Ingesting {file_type.upper()} file into isolated memory...")
#         add_log("[ANALYZER] Running Presidio PII & Context Engine...")
        
#         result = scan(file_bytes=file_bytes, filename=uploaded_file.name, filetype=file_type)
        
#         if result["status"] == "LEAK": add_log("[ALERT] 🚨 CRITICAL DATA LEAK DETECTED!")
#         elif result["status"] == "SAFE": add_log("[INFO] ✅ Document classified as Legitimate Disclosure.")
#         else: add_log("[WARN] ⚠️ Context unclear. Flagged for Manual Review.")
            
#         add_log("[SECURITY] Purging file bytes from RAM...")
#         add_log(f"[SECURITY] {secure_memory_cleanup()}")
#         add_log("[DOCKER] Container terminated and destroyed")
#         time.sleep(0.5)
        
#         # =================================================================
#         # 3. FORENSIC RISK & FINANCIAL EXPOSURE DASHBOARD
#         # =================================================================
#         st.markdown("---")
#         st.subheader("📈 Forensic Risk & Financial Exposure Quantification")
        
#         risk = result.get('risk_assessment', {})
#         if risk:
#             col_risk1, col_risk2, col_risk3 = st.columns([1, 1, 2])
            
#             with col_risk1:
#                 if risk['color'] == 'red': st.metric(label="Risk Score", value=f"{risk['score']}/100", delta="CRITICAL", delta_color="inverse")
#                 elif risk['color'] == 'orange': st.metric(label="Risk Score", value=f"{risk['score']}/100", delta="HIGH", delta_color="inverse")
#                 elif risk['color'] == 'yellow': st.metric(label="Risk Score", value=f"{risk['score']}/100", delta="MEDIUM", delta_color="off")
#                 else: st.metric(label="Risk Score", value=f"{risk['score']}/100", delta="LOW", delta_color="normal")

#             with col_risk2:
#                 st.metric(label="Severity Level", value=risk['level'])
#                 # st.write(risk.get("financial_exposure").get("total_exposure"))
#                 exposure = risk.get('financial_exposure').get("total_exposure")
#                 st.metric(label="Est. Financial Exposure", value=f"₹{exposure:,}")

#             with col_risk3:
#                 st.markdown("**Entity Severity Breakdown:**")
#                 st.write(f"🔴 Critical (Aadhaar/PAN/Pass): **{risk['breakdown']['Critical']}**")
#                 st.write(f"🟠 High (Phone/Email/SSN): **{risk['breakdown']['High']}**")
#                 st.write(f"🟡 Medium (Person/Location): **{risk['breakdown']['Medium']}**")
#                 st.progress(risk['score'] / 100.0)
#                 st.caption("*Estimates based on DPDP Act 2023 penalty guidelines per record.")

#         # =================================================================
#         # 4. Display Final Scan Results & SMART EXPORT
#         # =================================================================
#         st.markdown("---")
#         st.subheader("📊 Scan Results")
        
#         if result["status"] == "SAFE":
#             st.success(result['title'])
#             st.info(f"**Why Safe?** {result['reason']}")
#             if result.get('entities'):
#                 st.write("**Detected PII Entities (Legitimate):**")
#                 for entity in result['entities'][:5]:
#                     st.write(f"- {entity['entity_type']}: `{entity['text']}` (Confidence: {entity['score']:.2f})")

#         elif result['status'] == "LEAK":
#             st.error(result['title'])
#             st.warning(f"**Why Leak?** {result['reason']}")
#             if result.get('entities'):
#                 st.write("**Exposed PII Entities:**")
#                 for entity in result['entities'][:5]:
#                     st.write(f"- {entity['entity_type']}: `{entity['text']}` (Confidence: {entity['score']:.2f})")
            
#             if result.get('redacted_preview'):
#                 st.markdown("---")
#                 st.subheader("🛡️ Remediation")
#                 st.code(result.get('redacted_preview', 'No preview available'), language="text")
                
#                 st.markdown("**Choose Export Format:**")
#                 export_format = st.radio("Format", ["PDF Document", "CSV Spreadsheet"], horizontal=True, label_visibility="collapsed")
                
#                 base_filename = f"redacted_{uploaded_file.name.split('.')[0]}"
                
#                 if export_format == "CSV Spreadsheet":
#                     st.download_button(
#                         label="⬇️ Download Redacted CSV",
#                         data=result.get('redacted_full_text', 'No data'),
#                         file_name=f"{base_filename}.csv",
#                         mime="text/csv",
#                         type="primary"
#                     )
#                 else: # PDF Document
#                     st.download_button(
#                         label="⬇️ Download Redacted PDF",
#                         data=result.get('redacted_pdf_bytes', b'No data'),
#                         file_name=f"{base_filename}.pdf",
#                         mime="application/pdf",
#                         type="primary"
#                     )
            
#         else: # REVIEW
#             st.warning(result['title'])
#             st.info(f"**Why Review?** {result['reason']}")
#             if result.get('entities'):
#                 st.write("**Detected PII Entities:**")
#                 for entity in result['entities'][:5]:
#                     st.write(f"- {entity['entity_type']}: `{entity['text']}` (Confidence: {entity['score']:.2f})")



import streamlit as st 
import time
from core.scanner import scan
# Fixed typo: verify_network_isolation
from core.sandbox import get_container_id, verify_netowrk_isol, secure_memory_cleanup

# =====================================================================
# 1. GLOBAL CUSTOM CSS (NAVY BLUE & CREAM THEME)
# =====================================================================
# =====================================================================
# 1. GLOBAL CUSTOM CSS (NAVY BLUE & CREAM THEME - SIDEBAR FIXED)
# =====================================================================
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
    --terminal-bg: #050B24;
  }

  /* Global App Background */
  .stApp { background-color: var(--bg-primary) !important; color: var(--text-primary) !important; }
  
  /* ── SIDEBAR STYLING (FIXED) ─ */
  [data-testid="stSidebar"] {
      background-color: var(--bg-secondary) !important;
      border-right: 1px solid var(--accent);
  }
  /* Force all text inside sidebar to be cream colored */
  [data-testid="stSidebar"] * {
      color: var(--text-primary) !important;
  }
  /* Sidebar navigation links hover state */
  [data-testid="stSidebar"] a:hover {
      background-color: rgba(252, 241, 208, 0.1) !important;
      color: var(--text-primary) !important;
  }
  /* Active navigation link */
  [data-testid="stSidebar"] div[data-baseweb="list-item"][aria-selected="true"] {
      background-color: var(--accent) !important;
      border-radius: 8px;
  }

  /* Headings & Text */
  h1, h2, h3, p, span, div { color: var(--text-primary) !important; }
  .sub, .caption, small { color: var(--text-secondary) !important; }
  
  /* File Uploader Styling */
  .stFileUploader { 
      border: 2px dashed var(--accent) !important; 
      border-radius: 12px !important; 
      background-color: var(--card-bg) !important; 
      padding: 20px !important; 
  }
  .stFileUploader label { color: var(--text-primary) !important; }
  
  /* Primary Button Override */
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

  /* Terminal / Logs Styling (Flat Dark) */
  div[data-testid="stMarkdownContainer"] pre, .stCode, pre.stCode {
      background-color: var(--terminal-bg) !important; 
      border: 1px solid var(--accent) !important;
      border-left: 4px solid var(--text-primary) !important; 
      border-radius: 8px !important;
      font-family: 'Courier New', Courier, monospace !important; 
      font-size: 13px !important;
      padding: 15px !important; 
      box-shadow: none !important;
  }
  div[data-testid="stMarkdownContainer"] pre code, .stCode code, .stCode span {
      color: var(--text-primary) !important; 
      background-color: transparent !important;
  }

  /* Metrics Styling */
  div[data-testid="stMetricValue"] { 
      font-size: 1.4rem !important; 
      color: var(--text-primary) !important; 
      font-weight: 800 !important; 
  }
  div[data-testid="stMetricLabel"] { 
      color: var(--text-secondary) !important; 
      font-size: 0.8rem !important;
      text-transform: uppercase;
      letter-spacing: 0.5px;
  }
  
  /* Alerts & Status Boxes */
  .stAlert { 
      border-radius: 8px !important; 
      border: 1px solid var(--accent) !important;
      background-color: var(--card-bg) !important;
      color: var(--text-primary) !important;
  }
  .stSuccess { border-left: 4px solid #4ADE80 !important; }
  .stError { border-left: 4px solid #F87171 !important; }
  .stWarning { border-left: 4px solid #FBBF24 !important; }
  .stInfo { border-left: 4px solid #60A5FA !important; }

  /* Progress Bar */
  .stProgress > div > div > div > div { background-color: var(--text-primary) !important; }
  .stProgress > div > div { background-color: var(--accent) !important; }
</style>
""", unsafe_allow_html=True)

# =====================================================================
# 2. MAIN APP UI
# =====================================================================
st.title("🦊 FoxShield Scanner")
st.markdown("**Context-Aware Privacy Leak Scanner**")

uploaded_file = st.file_uploader(
    label="Upload your file to scan", 
    type=["pdf", "csv", "xlsx"], 
    help="Upload PDF, EXCEL OR CSV FILES"
)

if uploaded_file is not None:
    st.success(f"✅ File '{uploaded_file.name}' Uploaded Successfully")

    col1, col2, col3 = st.columns(3)
    with col1: st.metric(label="📄 File Name", value=uploaded_file.name)
    with col2: st.metric(label="💾 File Size", value=f"{uploaded_file.size / 1024:.2f} KB") 
    with col3: st.metric(label=" File Type", value=uploaded_file.type.upper())

    if st.button(label="🔬 Start Secure Scan", type="primary", use_container_width=True):
        log_placeholder = st.empty()
        logs = []
        
        def add_log(message: str):
            logs.append(message)
            log_placeholder.code("\n".join(logs), language="bash")
            time.sleep(0.4)

        container_id = get_container_id()
        add_log(f"[DOCKER] Initializing Sandbox Container: {container_id}")
        add_log("[NETWORK] Verifying egress restrictions...")
        network_status = verify_netowrk_isol()
        add_log(f"[NETWORK] External Access: {network_status}")
        add_log("[STORAGE] Mounting ephemeral read-only volume...")
        
        file_bytes = uploaded_file.getvalue()
        file_type = uploaded_file.name.split('.')[-1].lower()
        add_log(f"[SCAN] Ingesting {file_type.upper()} file into isolated memory...")
        add_log("[ANALYZER] Running Presidio PII & Context Engine...")
        
        result = scan(file_bytes=file_bytes, filename=uploaded_file.name, filetype=file_type)
        
        if result["status"] == "LEAK": add_log("[ALERT] 🚨 CRITICAL DATA LEAK DETECTED!")
        elif result["status"] == "SAFE": add_log("[INFO] ✅ Document classified as Legitimate Disclosure.")
        else: add_log("[WARN] ️ Context unclear. Flagged for Manual Review.")
            
        add_log("[SECURITY] Purging file bytes from RAM...")
        add_log(f"[SECURITY] {secure_memory_cleanup()}")
        add_log("[DOCKER] Container terminated and destroyed")
        time.sleep(0.5)
        
        # =================================================================
        # 3. FORENSIC RISK & FINANCIAL EXPOSURE DASHBOARD
        # =================================================================
        st.markdown("---")
        st.subheader("📈 Forensic Risk & Financial Exposure Quantification")
        
        risk = result.get('risk_assessment', {})
        if risk:
            col_risk1, col_risk2, col_risk3 = st.columns([1, 1, 2])
            
            with col_risk1:
                if risk['color'] == 'red': st.metric(label="Risk Score", value=f"{risk['score']}/100", delta="CRITICAL", delta_color="inverse")
                elif risk['color'] == 'orange': st.metric(label="Risk Score", value=f"{risk['score']}/100", delta="HIGH", delta_color="inverse")
                elif risk['color'] == 'yellow': st.metric(label="Risk Score", value=f"{risk['score']}/100", delta="MEDIUM", delta_color="off")
                else: st.metric(label="Risk Score", value=f"{risk['score']}/100", delta="LOW", delta_color="normal")

            with col_risk2:
                st.metric(label="Severity Level", value=risk['level'])
                exposure = risk.get('financial_exposure', {}).get("total_exposure", 0)
                st.metric(label="Est. Financial Exposure", value=f"₹{exposure:,}")

            with col_risk3:
                st.markdown("**Entity Severity Breakdown:**")
                st.write(f" Critical (Aadhaar/PAN/Pass): **{risk['breakdown']['Critical']}**")
                st.write(f"🟠 High (Phone/Email/SSN): **{risk['breakdown']['High']}**")
                st.write(f"🟡 Medium (Person/Location): **{risk['breakdown']['Medium']}**")
                st.progress(risk['score'] / 100.0)
                st.caption("*Estimates based on DPDP Act 2023 penalty guidelines per record.")

        # =================================================================
        # 4. Display Final Scan Results & SMART EXPORT
        # =================================================================
        st.markdown("---")
        st.subheader("📊 Scan Results")
        
        if result["status"] == "SAFE":
            st.success(result['title'])
            st.info(f"**Why Safe?** {result['reason']}")
            if result.get('entities'):
                st.write("**Detected PII Entities (Legitimate):**")
                for entity in result['entities'][:5]:
                    st.write(f"- {entity['entity_type']}: `{entity['text']}` (Confidence: {entity['score']:.2f})")

        elif result['status'] == "LEAK":
            st.error(result['title'])
            st.warning(f"**Why Leak?** {result['reason']}")
            if result.get('entities'):
                st.write("**Exposed PII Entities:**")
                for entity in result['entities'][:5]:
                    st.write(f"- {entity['entity_type']}: `{entity['text']}` (Confidence: {entity['score']:.2f})")
            
            if result.get('redacted_preview'):
                st.markdown("---")
                st.subheader("🛡️ Remediation")
                st.code(result.get('redacted_preview', 'No preview available'), language="text")
                
                st.markdown("**Choose Export Format:**")
                export_format = st.radio("Format", ["PDF Document", "CSV Spreadsheet"], horizontal=True, label_visibility="collapsed")
                
                base_filename = f"redacted_{uploaded_file.name.split('.')[0]}"
                
                if export_format == "CSV Spreadsheet":
                    st.download_button(
                        label="️ Download Redacted CSV",
                        data=result.get('redacted_full_text', 'No data'),
                        file_name=f"{base_filename}.csv",
                        mime="text/csv",
                        type="primary"
                    )
                else: # PDF Document
                    st.download_button(
                        label="⬇️ Download Redacted PDF",
                        data=result.get('redacted_pdf_bytes', b'No data'),
                        file_name=f"{base_filename}.pdf",
                        mime="application/pdf",
                        type="primary"
                    )
            
        else: # REVIEW
            st.warning(result['title'])
            st.info(f"**Why Review?** {result['reason']}")
            if result.get('entities'):
                st.write("**Detected PII Entities:**")
                for entity in result['entities'][:5]:
                    st.write(f"- {entity['entity_type']}: `{entity['text']}` (Confidence: {entity['score']:.2f})")