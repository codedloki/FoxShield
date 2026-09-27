from presidio_analyzer import AnalyzerEngine, PatternRecognizer, Pattern
from presidio_anonymizer import AnonymizerEngine
import pandas as pd
import pdfplumber
import io
import pytesseract
from pdf2image import convert_from_bytes
import logging

logger = logging.getLogger("FoxShield")

#==========================================================#
#                Engine Initialize                         #
# ==========================================================

analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()

# ✅ FIX 1: Correct spelling "AADHAAR_NUMBER" (2 A's)
aadhar_pattern = Pattern(regex=r"\b\d{4}[\s-]?\d{4}[\s-]?\d{4}\b", name="aadhaar_pattern", score=0.85)
aadhar_recognizer = PatternRecognizer(supported_entity="AADHAAR_NUMBER", patterns=[aadhar_pattern])

pan_pattern = Pattern(name="pan_pattern", regex=r"\b[A-Z]{5}[0-9]{4}[A-Z]{1}\b", score=0.85)
pan_recognizer = PatternRecognizer(supported_entity="PAN_CARD", patterns=[pan_pattern])

analyzer.registry.add_recognizer(aadhar_recognizer)
analyzer.registry.add_recognizer(pan_recognizer)


#==============================================================#
#                          File Extractors                    #
#=============================================================#

def extract_text_from_pdf(file_bytes: bytes) -> str:
    text = ""
    
    # 1. Try pdfplumber first
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    
    logger.info(f"📄 PDF Extraction Result: {len(text)} characters extracted")
    
    # 2. Fallback to OCR if no text found
    if not text.strip():
        logger.info("⚠️ No text found via pdfplumber. Switching to OCR (Tesseract) mode...")
        try:
            images = convert_from_bytes(file_bytes)
            logger.info(f"🖼️ Converted PDF to {len(images)} image(s) for OCR")
            
            for i, img in enumerate(images):
                # ✅ FIX 2: Added Hindi/Marathi support
                page_text = pytesseract.image_to_string(img, lang='eng+hin')
                text += page_text + "\n"
                logger.info(f"📝 OCR Page {i+1}: Extracted {len(page_text)} chars")
                
        except Exception as e:
            logger.error(f"❌ OCR Failed: {e}")
            return "OCR_FAILED"
    else:
        logger.info("✅ Text-based PDF detected, no OCR needed")
            
    logger.info(f" Total extracted text: {len(text)} characters")
    logger.info(f" First 100 chars: {text[:100]}")
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

def get_full_redacted_text(text: str, analyzer_results) -> str:
    """Returns COMPLETE redacted text for downloading"""
    anonymized = anonymizer.anonymize(text=text, analyzer_results=analyzer_results)
    return anonymized.text


#=======================================================================#
#               PDF Export Helper Function                              #
#=======================================================================#
def get_redacted_pdf_bytes(text: str) -> bytes:
    """Generates a PDF from redacted text. Requires 'reportlab'."""
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
        import io
        
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter
        c.setFont("Helvetica", 10)
        y = height - 50
        
        if not text.strip():
            text = "Document was empty or no text could be extracted."
            
        for line in text.split('\n'):
            wrapped_lines = [line[i:i+100] for i in range(0, len(line), 100)]
            for w_line in wrapped_lines:
                if y < 50:
                    c.showPage()
                    y = height - 50
                    c.setFont("Helvetica", 10)
                c.drawString(50, y, w_line)
                y -= 15
                
        c.save()
        return buffer.getvalue()
    except ImportError:
        return ("[NOTE: Install 'reportlab' for proper PDF export. This is plain text.]\n\n" + text).encode('utf-8')
    except Exception as e:
        return f"[PDF Generation Error: {e}]\n\n{text}".encode('utf-8')