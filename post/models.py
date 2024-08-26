from django.db import models
from django.urls import reverse
from django_ckeditor_5.fields import CKEditor5Field

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название')
    slug = models.CharField(max_length=256)
    main_post = models.OneToOneField('Post', related_name='main_in_category',
                                     on_delete=models.SET_NULL, null=True, blank=True)
    img = models.ImageField(default=None, upload_to='./main_post/',
                            verbose_name='Обложка главного поста', null=True, blank=True)

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
    content_ru = CKEditor5Field(config_name='extends', verbose_name='Контент на английском', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='posts', verbose_name='Категория')
    changed_by_manager = models.BooleanField(default=False)
    position_in_category = models.PositiveIntegerField(default=0, editable=False, verbose_name='Позиция в категории')

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
    
    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if self._state.adding:
            max_position = Post.objects.filter(category=self.category).aggregate(
                models.Max('position_in_category'))['position_in_category__max']
            print(max_position)
            self.position_in_category = 1 if max_position is None else max_position + 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        posts = list(Post.objects.filter(category=self.category))
        posts.pop(self.position_in_category - 1)
        for index, post in enumerate(posts, start=1):
            post.position_in_category = index
            post.save()
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


class Translations(models.Model):
    content_uz = CKEditor5Field(config_name='extends', verbose_name='Контент на узбекском')
    content_en = CKEditor5Field(config_name='extends', verbose_name='Контент на английском')

    class Meta:
        verbose_name = 'Перевод'
        verbose_name_plural = 'Переводы'