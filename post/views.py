from django.contrib.auth.decorators import permission_required
from django.shortcuts import render
from rest_framework import generics, renderers, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response

from user.permissions import IsSubscriberUser, IsManagerUser
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
    


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    renderer_classes = [renderers.JSONRenderer, renderers.TemplateHTMLRenderer]

    template_name = 'post.html'

    def get_permissions(self):
        if self.action in ['update', 'partial_update']:
            permission_classes = [IsManagerUser]
        elif self.action == 'retrieve':
            permission_classes = [IsSubscriberUser]
        elif self.action == 'destroy':
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if request.user.groups.filter(name='Manager').exists():
            instance.changed_by_manager = True
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
