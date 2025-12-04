from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm
from django.contrib.auth import logout
from django.conf import settings

User = get_user_model()


def signup_page(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)


        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)

    else:
        form = CustomUserCreationForm()

    return render(request, "accounts/signup.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")
