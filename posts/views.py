from django.shortcuts import render, redirect
from .models import Post

# Create your views here.


def all_posts(request):
    posts = Post.objects.all()

    return render(request, "all_posts.html", context={"posts": posts})


def create_post(request):
    if request.method == "POST":
        title = request.POST.get("title")
        body = request.POST.get("body")
        author = request.user

        post = Post.objects.create(title=title, body=body, author=author)
        post.save()
        return redirect("home")
    return render(request, "create_post.html")
