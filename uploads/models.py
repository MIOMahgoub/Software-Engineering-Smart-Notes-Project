from django.db import models
from accounts.models import CustomUser
from notes.models import Note

def upload_to(instance, filename):
    return f"uploads/{instance.user.id}/{filename}"

class UploadedFile(models.Model):
    FILE_TYPES = [
        ("pdf", "PDF Document"),
        ("docx", "Word Document"),
        ("txt", "Text File"),
        ("jpg", "Image (JPG)"),
        ("png", "Image (PNG)"),
    ]

    PROCESSING_STATUS = [
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("completed", "Completed"),
        ("failed", "Failed"),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="uploads")
    original_file = models.FileField(upload_to=upload_to)
    file_type = models.CharField(max_length=10, choices=FILE_TYPES)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    extracted_text = models.TextField(null=True, blank=True)
    processed_data = models.JSONField(null=True, blank=True)
    processing_status = models.CharField(max_length=20, choices=PROCESSING_STATUS, default="pending")
    ocr_used = models.BooleanField(default=False)

    # Links this upload to the generated Note (if processing succeeded)
    note = models.OneToOneField(Note, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.original_file.name} uploaded by {self.user.username}"

