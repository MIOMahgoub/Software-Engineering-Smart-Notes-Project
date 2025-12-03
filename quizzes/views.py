from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Quiz
from .services import grade_quiz

@login_required
def submit_quiz_view(request, quiz_id):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)

    quiz = get_object_or_404(Quiz, id=quiz_id)

    # expect data like {"answers": {"12": "34", "13": "40"}}
    data = request.POST  # or json.loads(request.body)
    # adapt this based on how front-end sends data
    raw_answers = data.get("answers", {})

    # Convert keys/values to ints
    answers = {int(qid): int(oid) for qid, oid in raw_answers.items()}

    qp = grade_quiz(request.user, quiz, answers)

    return JsonResponse({
        "score": qp.score,
        "correct": qp.correct_answers,
        "incorrect": qp.incorrect_answers,
    })


# Create your views here.
