from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from rest_framework.pagination import PageNumberPagination
from .models import Category, Post
from .serializers import CategorySerializer, PostSerializer


class BlogPagination(PageNumberPagination):
    page_size = 10


class PostListView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = BlogPagination

    def get_queryset(self):
        posts = Post.objects.filter(
            status=Post.Status.PUBLISHED
        ).select_related("author", "category")

        category = self.request.query_params.get("category")
        if category:
            posts = posts.filter(category__slug=category)

        return posts


class PostDetailView(generics.RetrieveAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "slug"
    queryset = Post.objects.filter(
        status=Post.Status.PUBLISHED
    ).select_related("author", "category")


class CategoryListView(generics.ListAPIView):
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]
    queryset = Category.objects.all()