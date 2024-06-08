from datetime import datetime
from django.core.exceptions import ValidationError
from user.models import Subscription
from user.validators import subscription_expired


def get_old_subscription(user):
    try:
        return Subscription.objects.get(user=user)
    except:
        return None


def validate(subscription):
    old_subscription = get_old_subscription(subscription['user'].id)
    if old_subscription:
        if old_subscription.subscription.name != "VIP":
            if subscription['is_active']:
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
                subscription['end_date'] = datetime(year=year, month=month,
                                             day=old_end_date.day, hour=old_end_date.hour,
                                             minute=old_end_date.minute, second=old_end_date.second,
                                             microsecond=old_end_date.microsecond)
            else:
                subscription['is_active'] = True
                subscription['start_date'] = datetime.today()
                period = subscription['subscription'].period
                month = subscription['start_date'].month + int(period)
                year = subscription['start_date'].year
                if month > 12:
                    month -= 12
                    year += 1
                subscription['end_date'] = datetime(year=year, month=month,
                                                    day=subscription['start_date'].day, hour=subscription['start_date'].hour,
                                                    minute=subscription['start_date'].minute, second=subscription['start_date'].second,
                                                    microsecond=subscription['start_date'].microsecond)
            return subscription
        raise ValidationError('You already have VIP subscription')
    return subscription

