from django.urls import path
from .views import RegisterAPIView
from .views import LoginAPIView

urlpatterns = [
    path("register", RegisterAPIView.as_view()),
    path("login", LoginAPIView.as_view())
]