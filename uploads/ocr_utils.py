import requests
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

OCR_URL = "https://api.ocr.space/parse/image"

def ocr_extract_text(filepath):
    """
    Sends image or PDF to OCR.Space and ALWAYS returns:
        (extracted_text, raw_response_dict)
    """
    api_key = getattr(settings, "OCR_SPACE_API_KEY", "")
    if not api_key:
        return "", {"error": "OCR API key missing"}

    try:
        with open(filepath, "rb") as f:
            response = requests.post(
                OCR_URL,
                files={"file": f},
                data={
                    "apikey": api_key,
                    "language": "eng",
                    "isOverlayRequired": False,
                },
                timeout=60
            )
    except Exception as e:
        logger.exception("OCR request failed")
        return "", {"error": str(e)}

    # Check HTTP status
    if response.status_code != 200:
        return "", {"error": f"HTTP {response.status_code}", "raw": response.text}

    # Parse JSON
    try:
        result = response.json()
    except Exception:
        return "", {"error": "Invalid JSON from OCR", "raw": response.text}

    # Processing error
    if result.get("IsErroredOnProcessing"):
        msg = result.get("ErrorMessage", ["Processing error"])
        if isinstance(msg, list):
            msg = msg[0]
        return "", {"error": msg, "raw": result}

    # Extract text
    parsed = result.get("ParsedResults") or []
    text = "\n\n".join([p.get("ParsedText", "") for p in parsed]).strip()

    if not text:
        return "", {"error": "No text found", "raw": result}

    return text, result
