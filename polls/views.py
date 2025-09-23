from django.shortcuts import render
from django.http import HttpResponse
from .models import Question


def index(request):
    latest = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": latest}
    return render(request, "polls/index.html", context)


def detail(request, question_id):
    context = {
        "question": Question.objects.get(pk=question_id),
        "error_message": "",
    }
    return render(request, "polls/detail.html", context)


def results(request, question_id):
    return HttpResponse(
        f"You're looking at the results of question {question_id}."
    )


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
