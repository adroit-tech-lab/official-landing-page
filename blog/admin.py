
# Register your models here.
from django.db import models
from django.contrib import admin
from .models import Category, Post
from django import forms
from tinymce.widgets import TinyMCE


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}

class PostAdminForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = "__all__"
        widgets = {
            "content": TinyMCE(),
            "excerpt": forms.Textarea(attrs={"rows": 3}),
        }

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "category", "status", "created_at")
    list_filter = ("status", "category")
    search_fields = ("title", "content")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("created_at", "updated_at")
    form = PostAdminForm
    formfield_overrides = {
    models.TextField: {"widget": TinyMCE()},
}
