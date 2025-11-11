from django.shortcuts import render
from django.core.mail import send_mail
from .forms import ContactForm


def index(request):
    return render(request, "contact/index.html", {"form": ContactForm()})


def submit(request):
    form = ContactForm(request.POST)
    if not form.is_valid():
        return render(request, "contact/index.html", {"form": form})
    data = form.cleaned_data
    send_mail(
        subject="Contact confirmation",
        message=(
            f"Hi {data['name']}, thank you for contacting us.\n"
            f"We will get back to you soon."
        ),
        from_email="from@example.com",
        recipient_list=[data["email"]],
        fail_silently=False,
    )
    return render(request, "contact/success.html", form.cleaned_data)
