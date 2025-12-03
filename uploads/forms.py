# uploads/forms.py

from django import forms
from .models import UploadedFile

class UploadForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ["file"]

    def clean_file(self):
        uploaded = self.cleaned_data["file"]
        allowed = ["pdf", "png", "jpg", "jpeg", "txt"]

        ext = uploaded.name.split(".")[-1].lower()
        if ext not in allowed:
            raise forms.ValidationError("Unsupported file type.")
        return uploaded
