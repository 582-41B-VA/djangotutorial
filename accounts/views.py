from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as django_login, logout as django_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


def register(request):
    return render(
        request, "accounts/register.html", {"form": UserCreationForm()}
    )


def register_submit(request):
    form = UserCreationForm(request.POST)
    if not form.is_valid():
        return render(request, "accounts/register.html", {"form": form})
    form.save()
    return redirect("accounts:login")


def login(request):
    return render(
        request, "accounts/login.html", {"form": AuthenticationForm()}
    )


def login_submit(request):
    form = AuthenticationForm(request, request.POST)
    if not form.is_valid():
        return render(request, "accounts/login.html", {"form": form})
    django_login(request, form.get_user())
    return redirect("accounts:detail")


def logout(request):
    django_logout(request)
    return redirect("accounts:login")


@login_required
def detail(request):
    return render(request, "accounts/detail.html")
