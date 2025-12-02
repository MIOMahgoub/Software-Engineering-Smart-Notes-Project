from django.contrib import admin
from .models import StudySession, QuizPerformance, TopicMastery
from accounts.models import CustomUser
from notes.models import Tag

@admin.register(StudySession)
class StudySessionAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "start_time",
        "end_time",
        "duration_minutes",
        "notes_used_count",
        "flashcards_reviewed_count",
        "quizzes_taken_count",
    )

    search_fields = ("user__username",)
    list_filter = ("start_time", "end_time", "user")

    readonly_fields = (
        "duration_minutes",
        "created_at",
        "notes_used_count",
        "flashcards_reviewed_count",
        "quizzes_taken_count",
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs if request.user.is_superuser else qs.filter(user=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user" and not request.user.is_superuser:
            kwargs["queryset"] = CustomUser.objects.filter(id=request.user.id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(QuizPerformance)
class QuizPerformanceAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "quiz",
        "score",
        "correct_answers",
        "incorrect_answers",
        "taken_at",
        "mastery_change",
    )

    search_fields = ("user__username", "quiz__title")
    list_filter = ("taken_at", "quiz")

    readonly_fields = (
        "score",
        "correct_answers",
        "incorrect_answers",
        "mastery_change",
        "taken_at",
    )

    def has_add_permission(self, request):
        return False  # No manual creation allowed
    
    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs if request.user.is_superuser else qs.filter(user=request.user)

@admin.register(TopicMastery)
class TopicMasteryAdmin(admin.ModelAdmin):
    list_display = ("user", "tag", "mastery_score", "last_updated")
    readonly_fields = ("mastery_score", "last_updated")
    list_filter = ("tag", "user")
    search_fields = ("user__username", "tag__name")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs if request.user.is_superuser else qs.filter(user=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == "user":
                kwargs["queryset"] = CustomUser.objects.filter(id=request.user.id)
            if db_field.name == "tag":
                kwargs["queryset"] = Tag.objects.filter(author=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # Prevent creating mastery scores manually
    def has_add_permission(self, request):
        return False

    # Prevent editing mastery scores manually
    def has_change_permission(self, request, obj=None):
        return False

