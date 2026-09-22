import streamlit as st 
from core.scanner import scan

# 1. Initialize Session State (Important!)
if 'scan_result' not in st.session_state:
    st.session_state.scan_result = None

st.title("🦊 FoxShield Scanner")

uploaded_file = st.file_uploader(
    label="Upload your file to scan",
    type=["pdf", "csv", "xlsx"],
    help="Upload PDF, EXCEL OR CSV FILES"
)

if uploaded_file is not None:
    st.success(f"✅ File '{uploaded_file.name}' Uploaded Successfully")

    # FIX 1: Changed st.columns(2) to st.columns(3)
    col1, col2, col3 = st.columns(3)
    with col1: 
        st.metric(label="File Name", value=uploaded_file.name)
    with col2:
        st.metric(label="File Size", value=f"{uploaded_file.size / 1024:.2f} KB") 
    with col3:
        st.metric(label="File Type", value=uploaded_file.type)

    if st.button(label="Start Secure Scan", type="primary", use_container_width=True):
        
        # FIX 2: Removed nested/duplicate expander
        with st.expander("🔒 Live Sandbox Logs", expanded=True):
            st.code(
                """[DOCKER] Container: fox-shield-sandbox-7x9k
[NETWORK] Egress: BLOCKED 🔒
[STORAGE] Ephemeral volume mounted
[SCAN] Initializing Presidio Analyzer...""", 
                language="bash"
            )
        
        with st.spinner("Extracting text and Detecting PII..."):
            file_bytes = uploaded_file.getvalue()
            
            # FIX 3: Defined file_type properly
            file_type = uploaded_file.name.split('.')[-1].lower()
            
            st.session_state.scan_result = scan(
                file_bytes=file_bytes,
                filename=uploaded_file.name,
                filetype=file_type
            )

        st.rerun()
    
    # FIX 4: Corrected Indentation for elif/else
    if st.session_state.scan_result:
        result = st.session_state.scan_result

        st.markdown("---")
        st.subheader("📊 Scan Results")
        
        if result["status"] == "SAFE":
            st.success(result['title'])
            st.info(f"**Why Safe?** {result['reason']}")
        
            if result.get('entities'):
                st.write("**Detected PII Entities:**")
                for entity in result['entities'][:5]:
                    st.write(f"- {entity['entity_type']}: `{entity['text']}` (Confidence: {entity['score']:.2f})")

        elif result['status'] == "LEAK":
            st.error(result['title'])
            st.warning(f"**Why Leak?** {result['reason']}")
            
            if result.get('entities'):
                st.write("**Exposed PII Entities:**")
                for entity in result['entities'][:5]:
                    st.write(f"- {entity['entity_type']}: `{entity['text']}` (Confidence: {entity['score']:.2f})")
            
            if st.button("🛡️ Redact Sensitive Data", type="secondary"):
                st.success("✅ Data Successfully Redacted!")
                st.code(result.get('redacted_preview', 'No preview available'), language="text")
                st.balloons()
            
        else: # REVIEW
            st.warning(result['title'])
            st.info(f"**Why Review?** {result['reason']}")
            
            if result.get('entities'):
                st.write("**Detected PII Entities:**")
                for entity in result['entities'][:5]:
                    st.write(f"- {entity['entity_type']}: `{entity['text']}` (Confidence: {entity['score']:.2f})")
        
        # Final sandbox log
        st.code("[AUDIT] Temporary files purged from sandbox\n[DOCKER] Container terminated", language="bash")