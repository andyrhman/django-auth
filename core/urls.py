from django.urls import path
from .views import RegisterAPIView, LoginAPIView, ForgotAPIView, ResetAPIView, UserAPIView, RefreshAPIView, LogoutAPIView

urlpatterns = [
    path("register", RegisterAPIView.as_view()),
    path("login", LoginAPIView.as_view()),
    path("user", UserAPIView.as_view()),
    path("refresh", RefreshAPIView.as_view()),
    path("logout", LogoutAPIView.as_view()),
    path("forgot", ForgotAPIView.as_view()),
    path("reset", ResetAPIView.as_view()),
]