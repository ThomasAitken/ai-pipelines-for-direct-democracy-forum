import os

import requests
from pypdf import PdfReader


def download_text_from_url(url: str) -> str:
    """
    Download and return the text from a URL.
    If it's a PDF, parse it accordingly.
    If it's an HTML page, parse out text.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
    except Exception as e:
        print(f"Failed to download from {url}. Error: {e}")
        return ""

    # Basic check for PDF vs HTML
    content_type = response.headers.get('Content-Type', '').lower()

    if 'application/pdf' in content_type or url.lower().endswith('.pdf'):
        # Write to a temporary file, then parse
        temp_pdf_path = "temp.pdf"
        with open(temp_pdf_path, 'wb') as f:
            f.write(response.content)

        extracted_text: list[str] = []
        try:
            pdf_reader = PdfReader(open(temp_pdf_path, 'rb'))
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                extracted_text.append(page.extract_text())
        except Exception as e:
            print(f"Error reading PDF from {url}. Error: {e}")
            return ""
        finally:
            # Clean up
            if os.path.exists(temp_pdf_path):
                os.remove(temp_pdf_path)

        return "\n".join(extracted_text)

    else:
        # HTML or plain text
        # If it's HTML, you may want to strip tags, or handle them carefully.
        # For simplicity, let's just return the raw text:
        return response.text