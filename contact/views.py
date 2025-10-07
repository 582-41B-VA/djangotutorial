from django.shortcuts import render
from .forms import ContactForm


def index(request):
    return render(request, "contact/index.html", {"form": ContactForm()})


def submit(request):
    form = ContactForm(request.POST)
    if not form.is_valid():
        return render(request, "contact/index.html", {"form": form})
    return render(request, "contact/success.html", form.cleaned_data)
