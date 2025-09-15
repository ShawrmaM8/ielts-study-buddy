# Purpose: Handle file reading (with optional translation, PDF reading)
import io
import docx

# Try to import pymupdf with error handling
try:
    import pymupdf
    PYMUPDF_AVAILABLE = True
except ImportError:
    PYMUPDF_AVAILABLE = False
    print("Warning: PyMuPDF not installed. PDF extraction will not be available.")

def extract_text(file):
    """Detect file type and extract text with error handling"""
    try:
        # Read file content once and store in memory
        file_content = file.read()
        file.seek(0)  # Reset file pointer for future reads

        if file.type == 'application/pdf':
            if not PYMUPDF_AVAILABLE:
                raise Exception("PDF extraction requires PyMuPDF to be installed. Please install it with: pip install pymupdf")
            return extract_text_from_pdf(file_content)
        elif file.type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
            return extract_text_from_docx(file_content)
        elif file.type == 'text/plain':
            return file_content.decode('utf-8')
        else:
            raise ValueError("Unsupported file type")
    except Exception as e:
        raise Exception(f"Error extracting text: {str(e)}")

def extract_text_from_pdf(file_content):
    """Extract text from PDF using pymupdf"""
    try:
        # Use pymupdf.open with stream for PDF content
        doc = pymupdf.open(stream=io.BytesIO(file_content), filetype='pdf')
        text = ''
        for page in doc:
            text += page.get_text()
        doc.close()
        return text
    except Exception as e:
        raise Exception(f"PDF extraction failed: {str(e)}")

def extract_text_from_docx(file_content):
    """Extract text from DOCX file"""
    try:
        doc = docx.Document(io.BytesIO(file_content))
        text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
        return text
    except Exception as e:
        raise Exception(f"DOCX extraction failed: {str(e)}")