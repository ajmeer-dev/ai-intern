# pdf_utils.py

import fitz  # PyMuPDF
import re

def extract_text_from_pdf(uploaded_file):
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_skills_from_text(text):
    # Very basic: extract section after "Skills" or "Technical Skills"
    pattern = r"(Skills|Technical Skills)[\s:]*([\s\S]*?)(?:\n\n|\Z)"
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        skills_text = match.group(2)
        # Split by comma or newline or dash
        skills = re.split(r"[,|\n|\u2022|-]+", skills_text)
        return [skill.strip() for skill in skills if skill.strip()]
    return []
