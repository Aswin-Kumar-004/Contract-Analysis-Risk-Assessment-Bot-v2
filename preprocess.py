from pypdf import PdfReader
from docx import Document
import re

def extract_text(file):
    try:
        if file.name.endswith(".pdf"):
            reader = PdfReader(file)
            text = " ".join(page.extract_text() for page in reader.pages)
            return text if text.strip() else "Empty PDF file detected."
        elif file.name.endswith(".docx"):
            doc = Document(file)
            text = " ".join(p.text for p in doc.paragraphs)
            return text if text.strip() else "Empty DOCX file detected."
        else:
            content = file.read()
            # Try multiple encodings
            for encoding in ['utf-8', 'latin-1', 'cp1252']:
                try:
                    return content.decode(encoding)
                except UnicodeDecodeError:
                    continue
            return content.decode('utf-8', errors='replace') # Fallback
    except Exception as e:
        return f"Error extracting text from {file.name}: {str(e)}"

def clean_text(text):
    text = re.sub(r"\n+", "\n", text)
    return text.strip()
