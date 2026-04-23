import io
import pdfplumber
import docx

SUPPORTED_EXTENSIONS = [".pdf", ".docx"]


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract plain text from a PDF file using pdfplumber."""
    text_parts = []
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text() or ""
            text_parts.append(page_text)
    return "\n".join(text_parts).strip()


def extract_text_from_docx(file_bytes: bytes) -> str:
    """Extract plain text from a DOCX file using python-docx."""
    doc = docx.Document(io.BytesIO(file_bytes))
    paragraphs = [paragraph.text for paragraph in doc.paragraphs if paragraph.text.strip()]
    return "\n".join(paragraphs).strip()


def extract_text_from_resume(uploaded_file) -> str:
    """Detect the uploaded resume type and extract plain text."""
    file_bytes = uploaded_file.read()
    file_name = uploaded_file.name.lower()
    if file_name.endswith(".pdf"):
        return extract_text_from_pdf(file_bytes)
    if file_name.endswith(".docx"):
        return extract_text_from_docx(file_bytes)
    raise ValueError("Unsupported file format. Please upload a PDF or DOCX file.")
