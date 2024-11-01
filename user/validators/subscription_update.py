from datetime import datetime
from django.core.exceptions import ValidationError
from user.models import Subscription

def get_old_subscription(user):
    try:
        return Subscription.objects.filter(user=user)
    except:
        return None


def validate(subscription):
    old_subscriptions = list(get_old_subscription(subscription['user'].id))
    active_sub = None
    for old_sub in old_subscriptions:
        if old_sub.is_active:
            active_sub = old_sub
    if old_subscriptions:
        if active_sub:
            if active_sub.subscription.name == "VIP":
                raise ValidationError('You already have VIP subscription')
            else:
                if subscription['subscription'].name == "VIP":
                    old_end_date = subscription['end_date']
                    year = 3000
                    month = old_end_date.month
                else:
                    new_period = subscription['subscription'].period
                    old_end_date = subscription['end_date']
                    month = old_end_date.month + int(new_period)
                    year = old_end_date.year
                    if month > 12:
                        month -= 12
                        year += 1
                try:
                    subscription['end_date'] = datetime(year=year, month=month,
                                         day=old_end_date.day, hour=old_end_date.hour,
                                         minute=old_end_date.minute, second=old_end_date.second,
                                         microsecond=old_end_date.microsecond)
                except ValueError:
                    subscription['end_date'] = datetime(year=year, month=month + 1,
                                                        day=1, hour=old_end_date.hour,
                                                        minute=old_end_date.minute, second=old_end_date.second,
                                                        microsecond=old_end_date.microsecond)
        else:
            if subscription['subscription'].name == "VIP":
                subscription['start_date'] = datetime.today()
            else:
                subscription['is_active'] = True
                subscription['start_date'] = datetime.today()
        return subscription
    return subscription

