from django.urls import path
from .views import all_posts, create_post

urlpatterns = [
    path("", all_posts, name="home"),
    path("posts/create/", create_post, name="create_post"),
]
