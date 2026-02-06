import pypdf

def extract_text_from_pdf(uploaded_file):
    """
    Extracts text from a PDF file object (Streamlit UploadedFile).
    """
    try:
        pdf_reader = pypdf.PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() or ""
        return text
    except Exception as e:
        return f"Error reading PDF: {str(e)}"