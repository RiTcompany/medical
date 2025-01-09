import datetime
import pytz
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import Token

from client.models import Client, ClientDevice
from medical_inventory import settings
from ..models import Subscription


def is_subscription_active():
    subscriptions = Subscription.objects.all()
    date = datetime.datetime.today().replace(tzinfo=pytz.timezone(settings.TIME_ZONE))
    for subscription in subscriptions:
        if subscription.is_active:
            end_date = subscription.end_date
            if end_date < date:
                subscription.is_active = False
                subscription.save()
                group_subscribers = Group.objects.get(name='Subscriber')
                group_subscribers.user_set.remove(subscription.user)
                group_subscribers = Group.objects.get(name='Member')
                group_subscribers.user_set.add(subscription.user)
                try:
                    client = Client.objects.get(user=subscription.user)
                    Token.objects.get(user=subscription.user).delete()
                    print(f'[{datetime.datetime.now()}] {subscription.user} token deleted (subscription expired)')
                    device = ClientDevice.objects.get(user=subscription.user, is_active=True)
                    device.is_active = False
                    device.save()
                    client.subscription_type = None
                    client.paid = False
                    client.save()
                except:
                    print(subscription.user)

    # raise ValidationError("You don't have subscription")

