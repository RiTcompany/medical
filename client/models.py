import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db import models
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import PermissionDenied, AuthenticationFailed

from user.models import SubscriptionType, Subscription
from user.subscription_serializer import SubscriptionSerializer

User = get_user_model()

# Create your models here.


class Client(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client', verbose_name='Пользователь')
    fcm_token = models.CharField(max_length=200, null=True, blank=True, verbose_name="Токен для Firebase")
    paid = models.BooleanField(default=False, verbose_name='Оплачено')
    subscription_type = models.ForeignKey(SubscriptionType, on_delete=models.CASCADE, null=True, default=None)

    def __str__(self):
        return self.user.username

    def get_active_subscription(self):
        try:
            return Subscription.objects.get(user=self.user, is_active=True)
        except:
            return None

    def get_token(self):
        try:
            return Token.objects.get(user=self.user)
        except:
            return None

    def end_date(self, subscription_type):
        date = datetime.datetime.today()
        if subscription_type.name == "VIP":
            year = 3000
            month = date.month
        else:
            month = date.month + int(subscription_type.period)
            year = date.year
            if month > 12:
                month %= 12
                year += 1
        try:
            end_date = datetime.datetime(year=year, month=month,
                                     day=date.day, hour=date.hour,
                                     minute=date.minute, second=date.second,
                                 microsecond=date.microsecond)
        except ValueError:
            end_date = datetime.datetime(year=year, month=month + 1,
                                     day=1, hour=date.hour,
                                     minute=date.minute, second=date.second,
                                 microsecond=date.microsecond)
        return end_date

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self._state.adding and self.subscription_type is not None:
            self.paid = True
            data = {}
            data['user'] = self.user.id
            data['subscription'] = self.subscription_type.id
            subscription = self.get_active_subscription()
            if subscription:
                data['end_date'] = subscription.end_date
                data['is_active'] = subscription.is_active
                serializer = SubscriptionSerializer(subscription, data=data)
                if serializer.is_valid():
                    serializer.save()
            else:
                data['end_date'] = self.end_date(self.subscription_type)
                print(data['end_date'])
                serializer = SubscriptionSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    group_subscribers = Group.objects.get(name='Subscriber')
                    group_subscribers.user_set.add(self.user)
        elif not self._state.adding and self.subscription_type is None:
            subscription = self.get_active_subscription()
            group_subscribers = Group.objects.get(name='Subscriber')
            group_subscribers.user_set.remove(self.user)
            token = self.get_token()
            if token:
                token.delete()
                print(f'[{datetime.datetime.now()}] "{self.user} token deleted (subscription expired)"')
            try:
                device = ClientDevice.objects.get(user=self.user, is_active=True)
                device.is_active = False
                device.save()
            except:
                pass
            if subscription:
                subscription.is_active = False
                subscription.save()
        return super().save(force_insert, force_update, using, update_fields)

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class ClientDevice(models.Model):
    device_id = models.CharField(max_length=128, editable=False)
    model = models.CharField(max_length=128, editable=False, null=True, default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False, related_name='devices')
    update_at = models.DateTimeField(auto_now=True)
    create_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    accessible = models.BooleanField(default=False, verbose_name="Имеет доступ к аккаунту")

    def __str__(self):
        return self.user.username

    def is_paid(self):
        if hasattr(self.user, 'client'):
            client = self.user.client.order_by('-id').first()
            if client:
                return client.paid
        return False

    class Meta:
        indexes = [
            models.Index(fields=['device_id'])
        ]
        verbose_name = 'Устройство'
        verbose_name_plural = 'Устройства'
        
    @classmethod
    def get_or_create_device(cls, user, device_id, model):
        user_devices = cls.objects.filter(user=user)
        if user_devices:
            user_devices_with_access = user_devices.filter(accessible=True)
            if user_devices_with_access:
                for user_device in user_devices_with_access:
                    if user_device.device_id == device_id and user_device.model == model:
                        if user_devices_with_access.filter(is_active=True):
                            raise PermissionDenied(
                                detail='Кечирсиз, сизнинг аккаунтингизга бирдан зиёд телефон орқали кирилган, бу бизнинг иловамизни истифода қилиш келишувига мувофик.')
                        user_device.is_active = True
                        user_device.save()
                        return user_device
                try:
                    device = user_devices.get(device_id=device_id, model__isnull=True)
                    device.model = model
                    if device.accessible:
                        device.is_active = True
                        device.save()
                        return device
                    else:
                        device.save()
                        raise PermissionDenied(
                            detail='Кечирсиз, сизнинг аккаунтингизга бирдан зиёд телефон орқали кирилган, бу бизнинг иловамизни истифода қилиш келишувига мувофик.')

                except:
                    device, created = cls.objects.get_or_create(user=user, device_id=device_id, model=model)
                    device.is_active = False
                    device.save()
                raise PermissionDenied(detail='Кечирсиз, сизнинг аккаунтингизга бирдан зиёд телефон орқали кирилган, бу бизнинг иловамизни истифода қилиш келишувига мувофик.')
            else:
                for user_device in user_devices:
                    if user_device.device_id == device_id and user_device.model == model:
                        user_device.accessible = True
                        user_device.is_active = True
                        user_device.save()
                        return user_device
                    try:
                        device = user_devices.get(device_id=device_id, model__isnull=True)
                        device.accessible = True
                        device.is_active = True
                        device.model = model
                        device.save()
                    except:
                        device, created = cls.objects.get_or_create(user=user, device_id=device_id,
                                                                    model=model)
                        device.accessible = True
                        device.is_active = True
                        device.save()
                    return device
        device = cls.objects.create(user=user, device_id=device_id, model=model)
        device.is_active = True
        device.accessible = True
        device.save()
        return device


    @classmethod
    def get_active_device(cls, user):
        try:
            return cls.objects.get(user=user, is_active=True)
        except cls.DoesNotExist:
            raise AuthenticationFailed(detail='Device with provided ID not found')
        except cls.MultipleObjectsReturned:
            cls.objects.filter(user=user).update(is_active=False)
            raise AuthenticationFailed(detail='Device with provided ID not found')

