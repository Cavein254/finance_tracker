from django.urls import path

from .views import LoginView, RegisterView, UserDetailView

urlspatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("me/<int:pk>", UserDetailView.as_view(), name="user-detail"),
]
