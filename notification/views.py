from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from .models import Notification
from .serializers import NotificationSerializer


class NotificationAPIView(ListAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def get_queryset(self):
        try:
            return Notification.objects.filter(recipient_group=self.request.user.groups.all()[0])
        except:
            return None
