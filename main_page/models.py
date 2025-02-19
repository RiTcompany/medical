from django.db import models

from post.models import Post
from post.transliterator import UzbekLanguagePack


class SocialMedia(models.Model):
    icon = models.ImageField(default=None, upload_to='./main_page/social_media/',
                            verbose_name='Иконка соцсети', null=True, blank=True)
    link = models.CharField(max_length=1000, verbose_name="Ссылка на соцсеть")

    class Meta:
        verbose_name = 'Социальная сеть'
        verbose_name_plural = 'Социальные сети'


class MainPage(models.Model):
    img = models.ImageField(default=None, upload_to='./main_page/social_media/',
                            verbose_name='Картинка на главной странице', null=True, blank=True)
    link = models.CharField(max_length=1000, null=True, blank=True, verbose_name="Ссылка")
    first_btn = models.CharField(max_length=100, verbose_name="Текст на первой кнопке")
    second_btn = models.CharField(max_length=100, verbose_name="Текст на второй кнопке")
    third_btn = models.CharField(max_length=100, verbose_name="Текст на третьей кнопке")
    first_btn_lat = models.CharField(max_length=100, default="", verbose_name="Текст на первой кнопке на латинице")
    second_btn_lat = models.CharField(max_length=100, default="", verbose_name="Текст на второй кнопке на латинице")
    third_btn_lat = models.CharField(max_length=100, default="", verbose_name="Текст на третьей кнопке на латинице")

    class Meta:
        verbose_name = 'Главная страница'
        verbose_name_plural = 'Главная страница'

class MainPageVideo(models.Model):
    link = models.CharField(max_length=1000, null=True, blank=True, verbose_name="Ссылка")

    class Meta:
        verbose_name = 'Видео на главной странице'
        verbose_name_plural = 'Видео на главной странице'


class Analysis(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название анализа")
    name_latin = models.CharField(max_length=100, verbose_name="Название анализа на латинице", null=True, blank=True)

    def transliterate_text(self, text):
        try:
            return UzbekLanguagePack().translit(text)
        except Exception as e:
            return e

    def save(self, *args, **kwargs):
        self.name_latin = self.transliterate_text(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Анализ"
        verbose_name_plural = "Анализы"


class Indicator(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название показателя")
    name_latin = models.CharField(max_length=100, verbose_name="Название анализа на латинице", null=True, blank=True)
    category = models.ForeignKey(Analysis, on_delete=models.CASCADE, related_name="indicators", verbose_name="Анализ")
    min_value = models.PositiveIntegerField(verbose_name="Минимальное значение")
    max_value = models.PositiveIntegerField(verbose_name="Максимальное значение")
    unit = models.CharField(max_length=100, verbose_name="Единица измерения")
    post = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True, related_name="indicators", verbose_name="Пост")

    def transliterate_text(self, text):
        try:
            return UzbekLanguagePack().translit(text)
        except Exception as e:
            return e

    def save(self, *args, **kwargs):
        self.name_latin = self.transliterate_text(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Показатель анализа'
        verbose_name_plural = 'Показатели анализа'
