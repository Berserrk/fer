import hashlib
import os
from docx import Document
import PyPDF2

def extract_text_from_docx(file_path):
    doc = Document(file_path)
    return '\n'.join([para.text for para in doc.paragraphs])

def extract_text_from_pdf(file_path):
    text = ''
    with open(file_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() or ''
    return text

def generate_document_hash(file_path):
    ext = os.path.splitext(file_path)[-1].lower()
    
    if ext == '.docx':
        content = extract_text_from_docx(file_path)
    elif ext == '.pdf':
        content = extract_text_from_pdf(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

    return hashlib.sha256(content.encode('utf-8')).hexdigest()
