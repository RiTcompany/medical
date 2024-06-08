from django.contrib import admin
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.authtoken.models import TokenProxy

from user.models import SubscriptionType, Subscription


class TokenAdmin(admin.ModelAdmin):
    search_fields = ['key', 'user__username']  # Add the key and related user's username to search_fields
    list_display = ['key', 'user']  # Customize the displayed fields

    def get_user(self, obj):
        return obj.user.username

    get_user.short_description = 'Username'

admin.site.register(Token, TokenAdmin)
admin.site.unregister(TokenProxy)

@admin.register(SubscriptionType)
class SubscriptionTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'period']

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'subscription', 'start_date', 'end_date', 'is_active']