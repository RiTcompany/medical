from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.models import TokenProxy

from user.models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("username", "email", "is_staff", "paid",)
    list_filter = ("username", "is_staff", "paid",)
    actions = ['delete_selected', 'access_selected', 'noaccess_selected']
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "password1", "password2", "is_staff",
                "is_active", "groups", "user_permissions"
            )}
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)

    def access_selected(self, request, queryset):
        queryset.update(paid=True)

    def noaccess_selected(self, request, queryset):
        queryset.update(paid=False)


admin.site.register(CustomUser, CustomUserAdmin)


class TokenAdmin(admin.ModelAdmin):
    search_fields = ['key', 'user__username']  # Add the key and related user's username to search_fields
    list_display = ['key', 'user']  # Customize the displayed fields

    def get_user(self, obj):
        return obj.user.username

    get_user.short_description = 'Username'

admin.site.register(Token, TokenAdmin)
admin.site.unregister(TokenProxy)
