from django.contrib import admin
from .models import Quiz, QuizQuestion, QuizOption, QuizResponse
from accounts.models import CustomUser
from notes.models import Note

class QuizOptionInline(admin.TabularInline):
    model = QuizOption
    extra = 2  # Provides 2 blank options by default
    max_num = 6


class QuizQuestionInline(admin.StackedInline):
    model = QuizQuestion
    extra = 1
    show_change_link = True


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "source_note", "created_at")
    search_fields = ("title", "user__username", "source_note__title")
    list_filter = ("created_at",)
    inlines = [QuizQuestionInline]

    readonly_fields = ("created_at",)

    # Users can only see their own quizzes
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs if request.user.is_superuser else qs.filter(user=request.user)

    # Users cannot choose someone else as the quiz owner
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:

            if db_field.name == "user":
                kwargs["queryset"] = CustomUser.objects.filter(id=request.user.id)

            if db_field.name == "source_note":
                kwargs["queryset"] = Note.objects.filter(author=request.user)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            form.base_fields["user"].disabled = True
        return form
    
    # Auto-set quiz owner
    def save_model(self, request, obj, form, change):
        if not obj.user_id:
            obj.user = request.user
        super().save_model(request, obj, form, change)
    




@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ("question_text", "quiz", "question_type", "created_at")
    search_fields = ("question_text", "quiz__title")
    list_filter = ("question_type",)
    inlines = [QuizOptionInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs if request.user.is_superuser else qs.filter(quiz__user=request.user)
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "quiz" and not request.user.is_superuser:
            kwargs["queryset"] = Quiz.objects.filter(user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)



@admin.register(QuizOption)
class QuizOptionAdmin(admin.ModelAdmin):
    list_display = ("option_text", "question", "is_correct")
    search_fields = ("option_text", "question__question_text")
    list_filter = ("is_correct",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs if request.user.is_superuser else qs.filter(question__quiz__user=request.user)
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "question" and not request.user.is_superuser:
            kwargs["queryset"] = QuizQuestion.objects.filter(quiz__user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)



@admin.register(QuizResponse)
class QuizResponseAdmin(admin.ModelAdmin):
    list_display = ("user", "question", "is_correct", "answered_at")
    search_fields = ("user__username", "question__question_text")
    list_filter = ("is_correct", "answered_at")
    readonly_fields = ("is_correct", "answered_at",)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs if request.user.is_superuser else qs.filter(user=request.user)


   
