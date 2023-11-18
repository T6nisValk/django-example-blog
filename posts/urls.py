from django.urls import path
from . import views

urlpatterns = [
    path("", views.PostsListView.as_view(), name="home"),
    path("posts/create/", views.create_post, name="create_post"),
    path("posts/<int:pk>", views.PostDetailView.as_view(), name="post_detail"),
    path("posts/<int:pk>/edit", views.edit_post, name="edit_post"),
]
