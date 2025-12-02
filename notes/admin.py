from django.contrib import admin
from .models import Note, Tag
from accounts.models import CustomUser

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "created_at")
    search_fields = ("title", "content", "author__username")
    list_filter = ("created_at",)
    readonly_fields = ("summary", "key_points", "is_processed")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "author" and not request.user.is_superuser:
            kwargs["queryset"] = CustomUser.objects.filter(id=request.user.id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        if not obj.author_id:
            obj.author = request.user
        super().save_model(request, obj, form, change)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "author")
    search_fields = ("name", "author__username")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs  # Admin sees all tags
        return qs.filter(author=request.user)  # Users see only their own tags

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Make "author" dropdown only show the current user
        if db_field.name == "author" and not request.user.is_superuser:
            kwargs["queryset"] = CustomUser.objects.filter(id=request.user.id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        # Auto-assign author when creating new tag
        if not obj.author_id:
            obj.author = request.user
        super().save_model(request, obj, form, change)
