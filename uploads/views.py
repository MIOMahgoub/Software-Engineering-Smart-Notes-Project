from django.shortcuts import render
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .ocr_utils import ocr_extract_text


from .models import UploadedFile

import requests
import logging

logger = logging.getLogger(__name__)


@login_required
def upload_page(request):
    """
    Displays the front-end upload UI.
    """
    return render(request, "uploads/upload_form.html")


def run_ocr_space(local_path, language="eng"):
    """
    Call OCR.Space API on a local file and return (text, raw_response_dict).
    If something goes wrong, returns (None, error_info_dict).
    """
    api_key = getattr(settings, "OCR_SPACE_API_KEY", "")
    endpoint = getattr(settings, "OCR_SPACE_ENDPOINT", "https://api.ocr.space/parse/image")

    if not api_key:
        logger.warning("OCR_SPACE_API_KEY is not set; skipping OCR.")
        return None, {"error": "OCR API key not configured"}

    try:
        with open(local_path, "rb") as f:
            files = {"file": f}
            data = {
                "language": language,
                "isOverlayRequired": False,
            }
            headers = {"apikey": api_key}

            resp = requests.post(endpoint, files=files, data=data, headers=headers, timeout=60)
    except Exception as e:
        logger.exception("Error calling OCR.Space")
        return None, {"error": str(e)}

    if resp.status_code != 200:
        return None, {
            "error": f"OCR API returned HTTP {resp.status_code}",
            "raw": resp.text[:1000],
        }

    try:
        payload = resp.json()
    except Exception as e:
        return None, {"error": f"Failed to parse JSON: {e}", "raw": resp.text[:1000]}

    if payload.get("IsErroredOnProcessing"):
        return None, {
            "error": payload.get("ErrorMessage") or "OCR indicated processing error",
            "details": payload,
        }

    parsed_results = payload.get("ParsedResults") or []
    texts = [r.get("ParsedText", "") for r in parsed_results]
    full_text = "\n\n".join(texts).strip()

    if not full_text:
        return None, {"error": "OCR returned empty text", "details": payload}

    return full_text, payload


@login_required
def process_upload(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required"}, status=400)

    uploaded_file = request.FILES.get("file")
    if not uploaded_file:
        return JsonResponse({"error": "No file provided"}, status=400)

    allowed_extensions = ["pdf", "png", "jpg", "jpeg"]
    extension = uploaded_file.name.split(".")[-1].lower()

    if extension not in allowed_extensions:
        return JsonResponse({"error": "Unsupported file type"}, status=400)

    # Save file
    storage = FileSystemStorage()
    saved_path = storage.save(uploaded_file.name, uploaded_file)

    # Create DB record in 'processing' state
    db_record = UploadedFile.objects.create(
        user=request.user,
        original_file=saved_path,
        file_type=extension,
        processing_status="processing",
        ocr_used=True,
    )

    # OCR PROCESSING SECTION

    file_path = storage.path(saved_path)
    extracted = ocr_extract_text(file_path)

    db_record.extracted_text = extracted
    db_record.processing_status = "completed"
    db_record.save()
    # END OCR PROCESSING

    return JsonResponse({
        "message": "File uploaded successfully",
        "file_id": db_record.id
    })


@login_required
def summary_page(request, file_id):
    """
    Displays the summary page for a given uploaded file.
    """
    file_obj = UploadedFile.objects.filter(
        id=file_id, user=request.user
    ).first()

    if not file_obj:
        return JsonResponse({"error": "File not found"}, status=404)

    summary_text = file_obj.extracted_text or "No text extracted yet (or OCR failed)."

    return render(request, "uploads/summary_page.html", {
        "file": file_obj,
        "summary": summary_text,
    })
