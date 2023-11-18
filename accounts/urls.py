from django.urls import path, include
from .views import register, profile

urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("register/", register, name="register"),
    path("profile/", profile, name="profile"),
]
