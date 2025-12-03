from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import StudySession, QuizPerformance, TopicMastery

@login_required
def analytics_dashboard(request):
    user = request.user

    study_count = StudySession.objects.filter(user=user).count()
    quizzes_taken = QuizPerformance.objects.filter(user=user).count()
    mastered_topics = TopicMastery.objects.filter(user=user, mastery_score__gte=80).count()

    context = {
        "study_count": study_count,
        "quizzes_taken": quizzes_taken,
        "mastered_topics": mastered_topics,
    }
    return render(request, "analytics/dashboard.html", context)


@login_required
def study_sessions(request):
    sessions = StudySession.objects.filter(user=request.user).order_by("-start_time")
    return render(request, "analytics/study_sessions.html", {"sessions": sessions})


@login_required
def quiz_performance(request):
    performances = QuizPerformance.objects.filter(user=request.user).order_by("-taken_at")
    return render(request, "analytics/quiz_performance.html", {"performances": performances})


@login_required
def topic_mastery(request):
    topics = TopicMastery.objects.filter(user=request.user).order_by("-mastery_score")
    return render(request, "analytics/topic_mastery.html", {"topics": topics})
