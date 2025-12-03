import requests
from django.conf import settings

OCR_URL = "https://api.ocr.space/parse/image"

def ocr_extract_text(filepath):
    """
    Sends image or PDF to OCR.Space and returns extracted text.
    """
    api_key = settings.OCR_SPACE_API_KEY
    if not api_key:
        return "OCR API key missing."

    with open(filepath, "rb") as f:
        response = requests.post(
            OCR_URL,
            files={"file": f},
            data={
                "apikey": api_key,
                "language": "eng"
            }
        )

    try:
        result = response.json()
    except:
        return "OCR service returned invalid response."

    if result.get("IsErroredOnProcessing"):
        return "OCR Error: " + result.get("ErrorMessage", ["Unknown error"])[0]

    parsed = result.get("ParsedResults")
    if not parsed:
        return "No text found."

    return parsed[0].get("ParsedText", "").strip()

