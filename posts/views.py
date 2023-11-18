from django.shortcuts import render, redirect, get_object_or_404
from .models import Post
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group, User
from django.contrib import messages
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse
from .forms import PostForm


class PostsListView(ListView):
    template_name = "all_posts.html"
    model = Post  # object
    context_object_name = "posts"  # context
    paginate_by = 4  # how many per page


class PostDetailView(LoginRequiredMixin, DetailView):
    template_name = "post_detail.html"
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_mod"] = self.request.user.groups.filter(name="moderators").exists()
        context["is_blocked"] = self.request.user.groups.filter(name="banned").exists()
        return context

    def post(self, request, *args, **kwargs):
        if "delete" in request.POST:
            post_to_delete = get_object_or_404(Post, pk=request.POST.get("delete"))
            post_to_delete.delete()
            return redirect("home")
        elif "ban_author" in request.POST:
            author_username = request.POST.get("ban_author")
            author = get_object_or_404(User, username=author_username)
            mod_group = Group.objects.get(name="moderators")
            banned = Group.objects.get(name="banned")
            mod_group.user_set.remove(author)
            banned.user_set.add(author)
            return redirect("home")
        elif "edit_post" in request.POST:
            return redirect(reverse("edit_post", kwargs={"pk": self.kwargs["pk"]}))
        return redirect("home")


class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    # Success_url = "/" or - models def get_absolute_url() - redirects
    permission_required = "posts.add_post"
    model = Post
    template_name = "post_form.html"
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostEditView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = "edit_post.html"
    model = Post
    template_name = "post_form.html"
    form_class = PostForm
