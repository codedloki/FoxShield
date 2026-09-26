# 🛡️ ContextShield / FoxShield

**CryptoFox · CodeX 2026 by MUSA · CX0207: Digital Identity, Analog Leak**

ContextShield is an offline-first privacy-leak scanner for government and municipal documents. It does not equate PII with a leak. It combines local PII detection with publication context, provenance, disclosure signals, field semantics and access level to produce **SAFE / NEEDS REVIEW / LEAK**, with an explanation.

## Implemented
- Python + FastAPI backend
- Python + Streamlit frontend with custom CSS
- PDF, XLSX and CSV ingestion
- PyMuPDF extraction with optional local Tesseract OCR fallback
- Local regex/custom recognizers, with Presidio/spaCy available as an offline enhancement path
- Aadhaar/PAN/phone/email/address-related detection signals and validation
- RTI/publication/provenance context analysis
- Configurable explainable risk scoring
- SQLite scan history
- Secure temporary scan workspace and raw-file deletion after processing
- PII-masked findings and non-PII logs
- Verified PDF redaction plus XLSX/CSV redaction
- JSON/audit downloads
- Automated tests
- Docker support with an internal network

## Architecture
`Streamlit → REST → FastAPI → ContextShield Engine → Ingestion / PII / Context / Risk / Reports / Redaction`

## Offline operation
Runtime processing makes no cloud AI, OCR, database, analytics, CDN, remote-font or external API calls. Install dependencies and any optional local OCR/model assets once, then run with network access disabled.

Presidio/spaCy are included in the dependency set, while deterministic local recognizers keep core scanning usable when a spaCy model is not installed. No model is downloaded during scanning.

## Setup

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -e .
```

Optional OCR support:
```bash
pip install -e '.[ocr]'
```

Generate synthetic fixtures:
```bash
python scripts/create_demo_data.py
```

Backend:
```bash
uvicorn foxshield.api.main:app --reload --port 8000
```

Frontend:
```bash
streamlit run src/foxshield/frontend/app.py --server.port 8501
```

Open `http://localhost:8501`. API docs are at `http://localhost:8000/docs`.

## Demo
1. `citizen_leak.xlsx`: Public + `/public/downloads/` + Unknown disclosure basis.
2. `rti_response.xlsx`: RTI + `/rti/disclosures/` + RTI Mandated.
3. `ambiguous.xlsx`: RTI-looking content but a conflicting public employee path.
4. `clean_document.csv`: no PII.

All values are synthetic.

## Security
- Upload size cap and file-signature checks.
- Filename sanitization and path traversal prevention.
- Random temporary scan workspace with restricted permissions.
- Raw uploads are not retained after scanning by default.
- Raw PII is not written to logs.
- Original files are never overwritten.
- Redacted PDF content is re-extracted to verify the sensitive values are gone.
- The prototype is not a legal decision engine and does not claim DPDP compliance.

## Risk model
Default prototype factors are configurable and are not legal standards:
- PII Sensitivity: 0–35
- Public Exposure: 0–20
- Missing Disclosure Basis: 0–20
- Context Mismatch: 0–15
- Provenance Uncertainty: 0–10

Default thresholds: 0–29 SAFE, 30–69 NEEDS REVIEW, 70–100 LEAK.

## Future scope
Municipal CMS integrations, additional Indian-language recognizers, authorized threat-intelligence integrations, federated learning, automated approval workflows and aggregate citizen dashboards are intentionally not represented as implemented features.
