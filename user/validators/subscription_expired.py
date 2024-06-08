import datetime

import pytz
from django.core.exceptions import ValidationError

from medical_inventory import settings
# from user.validators.subscription_update import get_old_subscription
from . import subscription_update

def is_subscription_active(user):
    subscription = subscription_update.get_old_subscription(user)
    if subscription:
        if not subscription.is_active:
            return
        date = datetime.datetime.today().replace(tzinfo=pytz.timezone(settings.TIME_ZONE))
        end_date = subscription.end_date
        if end_date < date:
            subscription.is_active = False
            subscription.save()
    # raise ValidationError("You don't have subscription")

