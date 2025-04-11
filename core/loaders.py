
from PyPDF2 import PdfReader

def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
    return text

def split_into_clauses(text):
    return [line.strip() for line in text.split('\n') if len(line.strip()) > 30]

def load_draft(file):
    text = extract_text_from_pdf(file)
    return split_into_clauses(text)
