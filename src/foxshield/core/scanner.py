import time
import pandas as pd 
import pdfplumber
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine 
from typing import Dict, List 
import io 
import re
#=======================================================================#
#               INITIALIZATION                                          #
#=======================================================================#
analyzer = AnalyzerEngine() 
anonymizer = AnonymizerEngine() 

#=======================================================================#
#               Context Keywords                                        #
#=======================================================================#
RTI_KEYWORDS = [
    "rti", "right to information", "public disclosure", 
    "transparency", "audit report", "gazette", "official",
    "section 4", "section 8", "public interest", "mandated",
    "published", "gazette notification", "government order"
]

LEAK_KEYWORDS = [
    "confidential", "internal use only", "draft", "private",
    "not for distribution", "restricted", "sensitive",
    "password", "credentials", "secret", "proprietary"
]

#=======================================================================#
#               File Extraction Functions                               #
#=======================================================================#
def extract_text_from_pdf(file_bytes: bytes) -> str:
    text = ""
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text 

def extract_text_from_excel(file_bytes: bytes) -> str:
    df = pd.read_excel(io.BytesIO(file_bytes))
    text = " | ".join(df.columns.astype(str)) + "\n"
    text += df.to_string(index=False)
    return text

def extract_text_from_csv(file_bytes: bytes) -> str:
    df = pd.read_csv(io.BytesIO(file_bytes))
    text = " | ".join(df.columns.astype(str)) + "\n"
    text += df.to_string(index=False)
    return text

#=======================================================================#
#               Redacted Preview Helper Function                        #
#=======================================================================#
def _get_redacted_preview(text: str, analyzer_results) -> str:
    anonymized = anonymizer.anonymize(text=text, analyzer_results=analyzer_results)
    preview = anonymized.text[:500]
    if len(text) > 500:
        preview += "..."
    return preview

#=======================================================================#
#               Main SCAN Function                                      #
#=======================================================================#
def scan(file_bytes: bytes, filename: str, filetype: str) -> Dict:
    
    if filetype == 'pdf':
        text = extract_text_from_pdf(file_bytes=file_bytes)
    elif filetype == "xlsx":
        text = extract_text_from_excel(file_bytes=file_bytes)
    elif filetype == "csv":
        text = extract_text_from_csv(file_bytes=file_bytes)
    else:
        return {"status": "ERROR", "title": "Invalid Filetype", "reason": "Only PDF, XLSX, CSV supported."}
    
    analyzer_result = analyzer.analyze(
        text=text,
        language="en",
        entities=["PERSON", "PHONE_NUMBER", "EMAIL_ADDRESS", "CREDIT_CARD", "US_SSN", "IP_ADDRESS", "LOCATION"]
    )

    pii_entities = []
    for r in analyzer_result:
        pii_entities.append({
            "entity_type": r.entity_type,
            "text": text[r.start:r.end],
            "score": r.score,
            "start": r.start,
            "end": r.end 
        })


#=============================================================================#
#               Password detection
#==============================================================================#

    password_pattern = r'\b[A-Za-z0-9@#$%^&*!+=]{8,}\b'
    passwords_found = re.findall(password_pattern, text)
        
    for pwd in passwords_found:
            # False positives avoid karnyasathi common words exclude kele
            exclude_words = [
                'CONFIDENTIAL', 'Internal', 'Distribution', 'Proprietary', 
                'Information', 'Department', 'Employee', 'Resources', 
                'Sensitive', 'Notification', 'Appointment', 'Transparency'
            ]
            
            if pwd not in exclude_words:
                # Jar Presidio ne aadhiach detect kela asel tar duplicate टाळण्यासाठी
                if not any(e['text'] == pwd for e in pii_entities):
                    pii_entities.append({
                        "entity_type": "PASSWORD",
                        "text": pwd,
                        "score": 0.95,
                        "start": text.find(pwd),
                        "end": text.find(pwd) + len(pwd)
                    })

    text_lower = text.lower()
    
    # ⚠️ IMPORTANT: He '1' (number one) ahe, 'l' (letter L) nahi!
    rti_score = sum(1 for keyword in RTI_KEYWORDS if keyword in text_lower)
    leak_score = sum(1 for keyword in LEAK_KEYWORDS if keyword in text_lower)

    if len(pii_entities) == 0:
        return {
            "status": "SAFE",
            "title": "🟢 NO PII DETECTED",
            "reason": "Document contains no personally identifiable information.",
            "entities": [],
            "redacted_preview": text[:500] + "..." if len(text) > 500 else text
        }
    
    if rti_score > leak_score and rti_score >= 1:
        return {
            "status": "SAFE",
            "title": "🟢 LEGITIMATE RTI DISCLOSURE",
            "reason": f"PII detected ({len(pii_entities)} entities), but document contains RTI/transparency indicators. Disclosure is legally mandated.",
            "entities": pii_entities[:10],
            "redacted_preview": text[:500] + "..." if len(text) > 500 else text
        }

    elif leak_score > rti_score and leak_score >= 1:
        return {
            "status": "LEAK",
            "title": "🔴 CRITICAL DATA LEAK",
            "reason": f"PII detected ({len(pii_entities)} entities) in document with confidentiality markers. Immediate redaction required!",
            "entities": pii_entities[:10],
            "redacted_preview": _get_redacted_preview(text, analyzer_result)
        }
    
    else:
        return {
            "status": "REVIEW",
            "title": "🟡 REQUIRES MANUAL REVIEW",
            "reason": f"PII detected ({len(pii_entities)} entities) but context is unclear. Please verify manually.",
            "entities": pii_entities[:10],
            "redacted_preview": _get_redacted_preview(text, analyzer_result)
        }