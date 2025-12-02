from django.contrib import admin
from .models import FlashcardDeck, Flashcard, FlashcardReviewLog
from accounts.models import CustomUser
from notes.models import Note


@admin.register(FlashcardDeck)
class FlashcardDeckAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "source_note", "created_at")
    search_fields = ("title", "user__username")
    list_filter = ("created_at",)

    readonly_fields = ("created_at",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs if request.user.is_superuser else qs.filter(user=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:

            if db_field.name == "user":
                kwargs["queryset"] = CustomUser.objects.filter(id=request.user.id)

            if db_field.name == "source_note":
                kwargs["queryset"] = Note.objects.filter(author=request.user)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        if not obj.user_id:
            obj.user = request.user
        super().save_model(request, obj, form, change)


@admin.register(Flashcard)
class FlashcardAdmin(admin.ModelAdmin):
    list_display = ("deck", "front_text", "created_at")
    search_fields = ("front_text", "deck__title")
    list_filter = ("deck",)

    readonly_fields = ("created_at",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs if request.user.is_superuser else qs.filter(deck__user=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "deck" and not request.user.is_superuser:
            kwargs["queryset"] = FlashcardDeck.objects.filter(user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(FlashcardReviewLog)
class FlashcardReviewLogAdmin(admin.ModelAdmin):
    list_display = ("user", "flashcard", "correct", "reviewed_at")
    readonly_fields = ("correct", "reviewed_at")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs if request.user.is_superuser else qs.filter(user=request.user)

    def has_add_permission(self, request):
        return False  # generated only by backend, not admin

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:

            if db_field.name == "user":
                kwargs["queryset"] = CustomUser.objects.filter(id=request.user.id)

            if db_field.name == "flashcard":
                from .models import Flashcard
                kwargs["queryset"] = Flashcard.objects.filter(deck__user=request.user)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)
