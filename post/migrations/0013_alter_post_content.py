# Generated by Django 4.2.6 on 2024-09-11 20:56

from django.db import migrations
import django_ckeditor_5.fields


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0012_alter_post_slug_alter_post_slug_lat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=django_ckeditor_5.fields.CKEditor5Field(blank=True, null=True, verbose_name='Контент'),
        ),
    ]
