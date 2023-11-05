from django.shortcuts import render, redirect
from .models import Post
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group, User
from django.contrib import messages


def all_posts(request):
    posts = Post.objects.all()

    return render(request, "all_posts.html", context={"posts": posts})


@permission_required("posts.edit_post", raise_exception=True)
@login_required
def edit_post(request, pk):
    post = Post.objects.get(pk=pk)
    title = post.title
    body = post.body
    if request.method == "POST":
        item_to_update = Post.objects.get(pk=pk)
        item_to_update.title = request.POST.get("title")
        item_to_update.body = request.POST.get("body")

        item_to_update.save()
        return redirect("home")
    return render(request, "edit_post.html", context={"title": title, "body": body})


@login_required
def post_detail(request, pk):
    post = Post.objects.get(pk=pk)
    is_mod = request.user.groups.filter(name="moderators").exists()
    is_blocked = request.user.groups.filter(name="banned").exists()
    if request.method == "POST":
        delete_id = request.POST.get("delete")
        ban_author = request.POST.get("ban_author")
        edit = request.POST.get("edit_post")
        if delete_id:
            post_to_delete = Post.objects.get(pk=delete_id)
            post_to_delete.delete()
        if ban_author:
            author = User.objects.filter(username=ban_author).first()
            mod_group = Group.objects.get(name="moderators")
            banned = Group.objects.get(name="banned")
            mod_group.user_set.remove(author)
            banned.user_set.add(author)
        if edit_post:
            return redirect(f"{pk}/edit")
        return redirect("home")
    return render(request, "post_detail.html", context={"post": post, "is_mod": is_mod, "is_blocked": is_blocked})


@permission_required("posts.add_post", raise_exception=True)
@login_required
def create_post(request):
    if request.method == "POST":
        title = request.POST.get("title")
        body = request.POST.get("body")
        author = request.user

        post = Post.objects.create(title=title, body=body, author=author)
        post.save()
        return redirect("home")
    return render(request, "create_post.html")
