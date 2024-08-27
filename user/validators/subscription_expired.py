import datetime
import pytz
from medical_inventory import settings
from ..models import Subscription


def is_subscription_active():
    subscriptions = Subscription.objects.all()
    for subscription in subscriptions:
        if subscription.is_active:
            date = datetime.datetime.today().replace(tzinfo=pytz.timezone(settings.TIME_ZONE))
            end_date = subscription.end_date
            if end_date < date:
                subscription.is_active = False
                subscription.save()
    # raise ValidationError("You don't have subscription")

