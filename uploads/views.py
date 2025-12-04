from django.shortcuts import render
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.conf import settings

from .ocr_utils import ocr_extract_text
from .huggingface_utils import summarize_text, extract_key_points, generate_flashcards, generate_quiz
from .models import UploadedFile

import logging
logger = logging.getLogger(__name__)



#   UPLOAD PAGE

@login_required
def upload_page(request):
    return render(request, "uploads/upload_form.html")


#   PROCESS FILE UPLOAD


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

    # Save the file
    storage = FileSystemStorage()
    saved_path = storage.save(uploaded_file.name, uploaded_file)
    file_path = storage.path(saved_path)

    # Create DB record
    db_record = UploadedFile.objects.create(
        user=request.user,
        original_file=saved_path,
        file_type=extension,
        processing_status="processing",
        ocr_used=True,
    )

    # PERFORM OCR

    try:
        extracted, raw_ocr = ocr_extract_text(file_path)
    except Exception as e:
        logger.exception("OCR failed")
        extracted = ""
        raw_ocr = {}

    if not extracted:
        extracted = "[OCR failed or returned no text.]"

    db_record.extracted_text = extracted

    #   AI TEXT GENERATION

    extracted_clean = extracted.strip()

    if extracted_clean:
        summary = summarize_text(extracted_clean)
        key_points = extract_key_points(extracted_clean)
        flashcards = generate_flashcards(extracted_clean)
        quiz = generate_quiz(extracted_clean)
    else:
        summary = "[No text extracted to summarize]"
        key_points = ""
        flashcards = ""
        quiz = ""

    db_record.summary = summary
    db_record.key_points = key_points
    db_record.flashcards = flashcards
    db_record.quiz = quiz
    db_record.processing_status = "done"
    db_record.save()

    return JsonResponse({
        "message": "File processed successfully",
        "file_id": db_record.id
    })


#       SUMMARY PAGE

@login_required
def summary_page(request, file_id):
    file_obj = UploadedFile.objects.filter(id=file_id, user=request.user).first()

    if not file_obj:
        return JsonResponse({"error": "File not found"}, status=404)

    return render(request, "uploads/summary_page.html", {
        "file": file_obj,
        "summary": file_obj.summary or "[No summary available]",
        "key_points": file_obj.key_points,
        "flashcards": file_obj.flashcards,
        "quiz": file_obj.quiz,
    })

    ''' old approach
    return render(request, "uploads/summary_page.html", {
        "file": file_obj,
        "summary": file_obj.summary or "[No summary available]"
    })
    '''
