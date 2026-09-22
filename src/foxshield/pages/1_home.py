import streamlit as st

st.title("🦊 Welcome to FoxShield 🦊")
st.markdown("""
**Context-Aware Privacy Leak Scanner for Government Portals**

FoxShield helps detect accidental PII exposure in PDFs and spreadsheets while distinguishing between legitimate transparency disclosures (like RTI responses) and actual data leaks.

### 🚀 How to use:
1. Go to the **🔍 Scan Portal** from the sidebar.
2. Upload a document or select a pre-loaded demo scenario.
3. View the context-aware analysis and redaction preview.
""")

st.info("💡 **Round 2 MVP Focus:** Proving contextual distinction (RTI vs. Leak) in a secure Docker sandbox.")
