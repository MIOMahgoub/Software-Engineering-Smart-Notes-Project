from django.contrib import admin
from .models import UploadedFile
from accounts.models import CustomUser

@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ("original_file", "user", "file_type", "processing_status", "uploaded_at")
    search_fields = ("original_file", "user__username")
    list_filter = ("file_type", "processing_status", "uploaded_at")

    readonly_fields = (
        "extracted_text",
        "processed_data",
        "file_type",     # prevent users from altering file_type
        "note",
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs if request.user.is_superuser else qs.filter(user=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user" and not request.user.is_superuser:
            kwargs["queryset"] = CustomUser.objects.filter(id=request.user.id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_form(self, request, obj=None, **kwargs):
        """Prevent non-admins from switching 'user' field."""
        form = super().get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            form.base_fields["user"].disabled = True
        return form

    def has_add_permission(self, request):
        """Uploads should only be created via the UI/API — not manually."""
        return False
