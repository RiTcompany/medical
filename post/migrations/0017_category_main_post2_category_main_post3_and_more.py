# Generated by Django 4.2.6 on 2024-09-23 15:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0016_alter_category_main_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='main_post2',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='main_in_category2', to='post.post', verbose_name='Главный пост 2'),
        ),
        migrations.AddField(
            model_name='category',
            name='main_post3',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='main_in_category3', to='post.post', verbose_name='Главный пост 3'),
        ),
        migrations.AlterField(
            model_name='category',
            name='main_post',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='main_in_category', to='post.post', verbose_name='Главный пост 1'),
        ),
    ]