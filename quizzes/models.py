from django.db import models
from accounts.models import CustomUser
from notes.models import Note


class Quiz(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="quizzes_created")
    title = models.CharField(max_length=255)
    source_note = models.ForeignKey(Note, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Quiz: {self.title} ({self.user.username})"


class QuizQuestion(models.Model):
    QUESTION_TYPES = [
        ("mcq", "Multiple Choice"),
        ("tf", "True/False"),
        ("short", "Short Answer")
    ]

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    question_text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES, default="mcq")
    difficulty = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Q: {self.question_text[:50]}..."


class QuizOption(models.Model):
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE, related_name="options")
    option_text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"Option for Q{self.question.id}: {self.option_text}"


class QuizResponse(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="quiz_responses")
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(QuizOption, on_delete=models.SET_NULL, null=True, blank=True)
    text_answer = models.TextField(null=True, blank=True)
    is_correct = models.BooleanField(default=False)
    answered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Response by {self.user.username} for Q{self.question.id}"

