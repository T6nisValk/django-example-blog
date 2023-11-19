from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=50)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} - {self.author}"

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"pk": self.pk})

    class Meta:
        verbose_name_plural = "!!!All the posts!!!"
        verbose_name = "!!!Some post!!!"
