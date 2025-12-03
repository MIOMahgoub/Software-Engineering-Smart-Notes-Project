from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.analytics_dashboard, name="analytics_dashboard"),
    path("study-sessions/", views.study_sessions, name="study_sessions"),
    path("quiz-performance/", views.quiz_performance, name="quiz_performance"),
    path("topic-mastery/", views.topic_mastery, name="topic_mastery"),
]
