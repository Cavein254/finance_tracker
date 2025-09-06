from rest_framework import generics

from .models import User
from .serializers import RegisterSerializer
from .tasks import send_welcome_email


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        send_welcome_email.delay(user.email)
