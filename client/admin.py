from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from .models import Client, ClientDevice

# Register your models here.

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):

    list_display = ('user_username', 'user_email', 'paid')

    actions = ['delete_selected', 'access_selected', 'noaccess_selected']

    search_fields = ['user__email', 'user__username']

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        qs = super().get_queryset(request)
        if request.user and request.user.groups.filter(name='Manager').exists():
            print(qs.first())
            return qs.exclude(user__is_staff=True)
        return qs

    def user_username(self, obj):
        return obj.user.username

    def user_email(self, obj):
        return obj.user.email

    def access_selected(self, request, queryset):
        queryset.update(paid=True)

    def noaccess_selected(self, request, queryset):
        queryset.update(paid=False)

    access_selected.short_description = "Give access selected clients"
    noaccess_selected.short_description = "Deny access selected clients"
    user_username.short_description = 'Логин'
    user_email.short_description = 'Почта'


@admin.register(ClientDevice)
class ClientDeviceAdmin(admin.ModelAdmin):
    list_display = ('device_id', 'is_active', 'user_username','user_email')

    actions = []

    search_fields = ['device_id', 'user__email', 'user__username']

    def user_username(self, obj):
        return obj.user.username

    def user_email(self, obj):
        return obj.user.email


