import os

import requests
from pypdf import PdfReader
from requests.adapters import HTTPAdapter, Retry


def download_text_from_url(session: requests.Session, url: str) -> str:
    """
    Download and return the text from a URL.
    If it's a PDF, parse it accordingly.
    If it's an HTML page, parse out text.
    """
    try:
        response = session.get(url)
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
    

def get_requests_session():
    # The main motivation for this class was retrying on NameResolutionErrors
    # This automatically triggers retries for NameResolutionErrors without any config
    retries = Retry(
        total=5,
        backoff_factor=1,
        status_forcelist=[500, 502, 503, 504],
        allowed_methods=None,
        raise_on_redirect=True,
        raise_on_status=True,
    )
    session = requests.Session()
    session.headers.update(
        {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0"}
    )
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("https://", adapter)
    return session