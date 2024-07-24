from django.shortcuts import render
from rest_framework import generics, renderers

from user.permissions import IsSubscriberUser
from .models import (
    Category,
    Post
)

from .serializers import (
    CategorySerializer,
    PostSerializer
)

# Create your views here.

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        startswith = self.request.query_params.get('startswith')
        if startswith:
            queryset = queryset.filter(name__istartswith=startswith)
        
        queryset = queryset.exclude(id=180)
        return queryset
    

class CategoryView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    
class PostListView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.request.query_params.get('category_id')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        q = self.request.query_params.get('q')
        print(q)
        if q:
            queryset = queryset.filter(name__iregex=q)
            print(queryset)
        return queryset
    

class PostView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    renderer_classes = [renderers.JSONRenderer, renderers.TemplateHTMLRenderer]
    permission_classes = [IsSubscriberUser]

    template_name = 'post.html'