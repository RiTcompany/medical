# Generated by Django 4.2.6 on 2024-10-07 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0002_alter_notification_recipient_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='recipient_group',
            field=models.CharField(blank=True, choices=[('Manager', 'Manager')], max_length=100, null=True, verbose_name='Группа получателей'),
        ),
    ]
