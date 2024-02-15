from django.contrib.auth import get_user_model
from django.db import models
from rest_framework.exceptions import PermissionDenied, AuthenticationFailed

User = get_user_model()

# Create your models here.

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='client', verbose_name='Пользователь')
    paid = models.BooleanField(default=False, verbose_name='Оплачено')
    
    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class ClientDevice(models.Model):
    device_id = models.CharField(max_length=128)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='devices')
    update_at = models.DateTimeField(auto_now=True)
    create_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['device_id']),
            models.Index(fields=['device_id', 'is_active'])
        ]
        unique_together = ('user', 'device_id')
        verbose_name = 'Устройство'
        verbose_name_plural = 'Устройства'
        
    @classmethod
    def get_or_create_device(cls, user, device_id):
        if cls.objects.filter(device_id=device_id, is_active=True).exists():
            raise PermissionDenied(detail='Кечирсиз, бир телефондан фақат бир аккаунтга кириш мумкин, илтимос, иккинчи аккаунтинтдан чикинг.') 
        user_devices = cls.objects.filter(user=user)
        if user_devices.filter(is_active=True).count() >= 1 and not user.username == 'user':
            raise PermissionDenied(detail='Кечирсиз, сизнинг аккаунтингизга бирдан зиёд телефон орқали кирилган, бу бизнинг иловамизни истифода қилиш келишувига мувофик.') 

        device, created = cls.objects.get_or_create(user=user, device_id=device_id)
        device.is_active = True
        device.save()
        return device
                

    @classmethod
    def get_active_device(cls, device_id):
        try: 
            return cls.objects.get(device_id=device_id, is_active=True)
        except cls.DoesNotExist:
            raise AuthenticationFailed(detail='Device with provided ID not found')
        except cls.MultipleObjectsReturned:
            cls.objects.filter(device_id=device_id).update(is_active=False)
            raise AuthenticationFailed(detail='Device with provided ID not found')
            
