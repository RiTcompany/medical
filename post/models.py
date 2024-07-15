from django.db import models
from django.urls import reverse
from django_ckeditor_5.fields import CKEditor5Field

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название')
    slug = models.CharField(max_length=256)
     
    def __str__(self):
        return self.name
    
    def generate_slug(self):
        return self.name.lower()
    
    def save(self, *args, **kwargs):
        self.slug = self.generate_slug()
        super().save(*args, **kwargs)
        
    def get_absolute_url(self):
        return reverse('category-detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        

class Post(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    update_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    published = models.BooleanField(verbose_name='Опубликован')
    content = CKEditor5Field(config_name='extends', verbose_name='Контент')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='posts', verbose_name='Категория')
    changed_by_manager = models.BooleanField(default=False)
    
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
    
    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
