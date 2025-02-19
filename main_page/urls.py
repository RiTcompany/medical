from django.urls import path
from . import views


urlpatterns = [
    path('analysis', views.AnalysisListAPIView.as_view(), name='analysis-list'),
    path('analysis/<int:pk>', views.AnalysisAPIView.as_view(), name='analysis-detail'),
    path('', views.MainPageAPIView.as_view(), name='main_page')
]