from django.contrib import admin
from .models import Post
import django.apps


class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at", "updated_at", "author")
    fieldsets = (
        "post info",
        {"fields": ("title", "body")},
    ), (
        "Author info",
        {"fields": ("author",)},
    )


admin.site.register(Post, PostAdmin)

models = django.apps.apps.get_models()

for model in models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass
