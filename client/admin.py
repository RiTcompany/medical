from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from .models import Client, ClientDevice

# Register your models here.

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('user_username', 'paid', 'subscription_type')

    actions = ['deactivate_subscription']

    search_fields = ['user__email', 'user__username']

    def group_manager_exist(self, request):
        try:
            return request.user.groups.filter(name="Manager").exists()
        except:
            return False

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        qs = super().get_queryset(request)
        if request.user and self.group_manager_exist(request):
            return qs.exclude(user__is_staff=True)
        return qs

    def user_username(self, obj):
        return obj.user.username

    def user_email(self, obj):
        return obj.user.email

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super(ClientAdmin, self).get_actions(request)
        try:
            del actions['delete_selected']
            return actions
        except:
            return actions

    def save_model(self, request, obj, form, change):
        if "paid" in form.changed_data and not obj.paid:
            obj.subscription_type = None
        return super().save_model(request, obj, form, change)

    def deactivate_subscription(self, obj, queryset):
        for obj in queryset:
            if obj.paid:
                obj.paid = False
                obj.subscription_type = None
                obj.save()

    deactivate_subscription.short_description = 'Деактивировать подписку'
    user_username.short_description = 'Логин'
    user_email.short_description = 'Почта'


@admin.register(ClientDevice)
class ClientDeviceAdmin(admin.ModelAdmin):
    list_display = ('device_id', 'is_active', 'user_username', 'user_email')

    actions = []

    search_fields = ['device_id', 'user__email', 'user__username']

    def user_username(self, obj):
        return obj.user.username

    def user_email(self, obj):
        return obj.user.email
