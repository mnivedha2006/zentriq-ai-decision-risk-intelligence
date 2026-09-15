import os
import fitz
import docx

def extract_text_from_file(file_path: str) -> str:
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()
    text = ""
    if ext == ".pdf":
        with fitz.open(file_path) as doc:
            for page in doc:
                text += page.get_text()
    elif ext == ".docx":
        doc = docx.Document(file_path)
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
    elif ext == ".txt":
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
    else:
        raise ValueError(f"Unsupported file format: {ext}")
    return text.strip()