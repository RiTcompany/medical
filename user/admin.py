from django.contrib import admin
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.authtoken.models import TokenProxy


class TokenAdmin(admin.ModelAdmin):
    search_fields = ['key', 'user__username']  # Add the key and related user's username to search_fields
    list_display = ['key', 'user']  # Customize the displayed fields

    def get_user(self, obj):
        return obj.user.username

    get_user.short_description = 'Username'

admin.site.register(Token, TokenAdmin)
admin.site.unregister(TokenProxy)
