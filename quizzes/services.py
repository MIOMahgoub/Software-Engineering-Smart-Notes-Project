# quizzes/services.py

from typing import Dict, List
from django.db import transaction

from accounts.models import CustomUser
from .models import Quiz, QuizQuestion, QuizOption, QuizResponse
from analytics.models import QuizPerformance, TopicMastery
from notes.models import Tag

@transaction.atomic
def grade_quiz(user: CustomUser, quiz: Quiz, answers: Dict[int, int]) -> QuizPerformance:
    """
    answers: {question_id: selected_option_id}
    """
    questions = quiz.questions.all()
    total_questions = questions.count()

    correct = 0
    incorrect = 0

    # Create responses
    for question in questions:
        selected_option_id = answers.get(question.id)
        selected_option = None

        if selected_option_id:
            selected_option = QuizOption.objects.filter(
                id=selected_option_id, question=question
            ).first()

        is_correct = bool(selected_option and selected_option.is_correct)

        if is_correct:
            correct += 1
        else:
            incorrect += 1

        QuizResponse.objects.create(
            user=user,
            question=question,
            selected_option=selected_option,
            is_correct=is_correct,
        )

    score = (correct / total_questions * 100.0) if total_questions > 0 else 0.0

    # Create performance record
    qp = QuizPerformance.objects.create(
        user=user,
        quiz=quiz,
        score=score,
        correct_answers=correct,
        incorrect_answers=incorrect,
        mastery_change=0.0,  # will be updated below
    )

    # Update topic mastery
    update_topic_mastery_from_quiz(user, quiz, qp)

    return qp


def update_topic_mastery_from_quiz(user: CustomUser, quiz: Quiz, performance: QuizPerformance):
    """
    Simple placeholder logic:
    - For each tag used in the quiz's source_note
    - Nudge mastery score up/down based on score.
    """
    if not quiz.source_note:
        return

    tags = quiz.source_note.tags.all()
    score = performance.score

    for tag in tags:
        tm, created = TopicMastery.objects.get_or_create(
            user=user,
            tag=tag,
            defaults={"mastery_score": 0.0},
        )

        # Very simple adjustment: move 10% toward score
        # new = old + 0.1 * (score - old)
        new_mastery = tm.mastery_score + 0.1 * (score - tm.mastery_score)
        tm.mastery_score = max(0.0, min(100.0, new_mastery))
        tm.save()

        # Track the change on QuizPerformance (optional: avg change)
        performance.mastery_change = new_mastery - tm.mastery_score
        performance.save()
