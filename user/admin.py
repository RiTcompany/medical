from django.contrib import admin
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User, Group
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

    actions = ['delete_model', 'publish_selected', 'unpublish_selected']

    def get_actions(self, request):
        actions = super(SubscriptionAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def delete_model(self, request, obj):
        for o in obj.all():
            group_subscribers = Group.objects.get(name='Subscriber')
            group_subscribers.user_set.remove(o.user)
            o.delete()

    delete_model.short_description = 'Удалить выбранные подписки'