from django.urls import path
from .views import CategoryListView, PostDetailView, PostListView

urlpatterns = [
    path("posts/", PostListView.as_view(), name="post-list"),
    path("posts/<slug:slug>/", PostDetailView.as_view(), name="post-detail"),
    path("categories/", CategoryListView.as_view(), name="category-list"),
]