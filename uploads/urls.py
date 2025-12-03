from django.urls import path
from . import views

app_name = "uploads"

urlpatterns = [
    path("", views.upload_page, name="upload_page"),  
    path("process/", views.process_upload, name="process_upload"),
    path("summary/<int:file_id>/", views.summary_page, name="summary_page"),
]
