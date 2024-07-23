from django.urls import include, path
from . import views

urlpatterns = [
    path('categories', views.CategoryListView.as_view(), name='category-list'),
    path('categories/<int:pk>', views.CategoryView.as_view(), name='category-detail'),
    path('', views.PostListView.as_view(), name='post-list'),
    path('<int:pk>', views.PostAPIDetail.as_view(), name='post-detail'),
    path('update/<int:pk>', views.PostAPIUpdate.as_view(), name='post-update'),
    path('delete/<int:pk>', views.PostAPIDestroy.as_view(), name='post-delete'),
]
