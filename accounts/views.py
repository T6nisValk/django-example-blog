from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import User


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")

        if password != password2:
            messages.error(request, "Passwords do not match.")
            return redirect("register")

        if len(username) < 4:
            messages.error(request, "Username must be at least 4 characters long.")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "User already exists.")
            return redirect("register")

        User.objects.create_user(username=username, password=password)
        return redirect("login")

    return render(request, "registration/register.html")
