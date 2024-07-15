from django.urls import include, path
from . import views

urlpatterns = [
    path('categories', views.CategoryListView.as_view(), name='category-list'),
    path('categories/<int:pk>', views.CategoryView.as_view(), name='category-detail'),
    path('', views.PostListView.as_view(), name='post-list'),
    path('<int:pk>', views.PostView.as_view({'get': 'list', 'put': 'update'}), name='post-detail'),
]
