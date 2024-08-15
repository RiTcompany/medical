from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Notification
from .serializers import NotificationSerializer

class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Возвращаем уведомления только для текущего пользователя
        return Notification.objects.filter(recipient=self.request.user)

    def perform_create(self, serializer):
        # Автоматически указываем получателя уведомления как текущего пользователя
        serializer.save(recipient=self.request.user)
