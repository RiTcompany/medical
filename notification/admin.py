from django.contrib import admin

from client.models import Client
from notification.firebase_service import FirebaseService
from notification.models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'message', 'post', 'recipient_group', 'created_at')

    def save_model(self, request, obj, form, change):
        clients = Client.objects.filter(fcm_token__isnull=False)
        obj.save()
        for client in clients:
            if client.user.groups.filter(name=obj.recipient_group).exists():
                FirebaseService.send_push_notification(fcm_token=client.fcm_token, title=obj.title, body=obj.message)
