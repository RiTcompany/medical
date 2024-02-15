from django.urls import path
from .views import *

urlpatterns = [
    path('sign_in', SignInView.as_view()),
    path('sign_up', SignUpView.as_view()),
    path('sign_out', SignOutView.as_view()),
    path('me', MeView.as_view()),
    path('token/login', TokenLogin.as_view()),
    path('token/logout', TokenLogout.as_view()),
    path('token/me', TokenMe.as_view()),
]
