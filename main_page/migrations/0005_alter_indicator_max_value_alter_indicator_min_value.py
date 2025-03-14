# Generated by Django 4.2.6 on 2025-03-13 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_page', '0004_analysis_indicator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='indicator',
            name='max_value',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Максимальное значение'),
        ),
        migrations.AlterField(
            model_name='indicator',
            name='min_value',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Минимальное значение'),
        ),
    ]
