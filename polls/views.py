from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Choice, Question


def index(request):
    latest = Question.objects.order_by("-pub_date")[:5]  # should be in models
    context = {"latest_question_list": latest}
    return render(request, "polls/index.html", context)


def detail(request, question_id):
    context = {
        "question": get_object_or_404(Question, pk=question_id),
        "error_message": "",
    }
    return render(request, "polls/detail.html", context)


def results(request, question_id):
    return HttpResponse(
        f"You're looking at the results of question {question_id}."
    )


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        choice_id = request.POST["choice"]
        selected_choice = question.choice_set.get(pk=choice_id)
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("results", args=(question.id,)))
