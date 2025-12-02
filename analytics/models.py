from django.db import models
from accounts.models import CustomUser
from notes.models import Tag
from quizzes.models import Quiz


class StudySession(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="study_sessions")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField()
    notes_used_count = models.PositiveIntegerField(default=0)
    flashcards_reviewed_count = models.PositiveIntegerField(default=0)
    quizzes_taken_count = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Study session by {self.user.username} on {self.start_time.date()}"


class QuizPerformance(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="quiz_performance")
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.FloatField()
    correct_answers = models.PositiveIntegerField()
    incorrect_answers = models.PositiveIntegerField()
    mastery_change = models.FloatField(default=0.0)

    taken_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} scored {self.score}% on {self.quiz.title}"


class TopicMastery(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="topic_mastery")
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name="topic_mastery")
    mastery_score = models.FloatField(default=0.0)  # 0 to 100 suggested range
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "tag")

    def __str__(self):
        return f"{self.user.username} mastery in {self.tag.name}: {self.mastery_score}"
