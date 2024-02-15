from django.contrib import admin
from django_admin_listfilter_dropdown.filters import DropdownFilter, ChoiceDropdownFilter, RelatedOnlyDropdownFilter

from .models import (
    Category,
    Post
)

# Register your models here.

class NameStartsWithFilter(admin.SimpleListFilter):
    title = "Name starts with"
    parameter_name = 'name__startswith'
    
    def lookups(self, request, model_admin):
        names = Category.objects.values_list('name', flat=True).distinct()
        return [(name[0].upper(), name[0].lower()) for name in names]
    
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(slug__istartswith=self.value().lower())
        return queryset
    
    
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    exclude = ('slug',)
    search_fields = ['name', 'slug']
    
    list_filter = (NameStartsWithFilter,)
    
    def custom_delete_selected(self, request, queryset):
        for obj in queryset:
            obj.delete()

    custom_delete_selected.short_description = 'Удалить выбранные категории'

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('name', 'category_name', 'create_at', 'update_at', 'published')
    search_fields = ['name', 'category__slug']
    list_filter = [('category', RelatedOnlyDropdownFilter), 'published']
    

    actions = ['custom_delete_selected', 'publish_selected', 'unpublish_selected']

    def category_name(self, obj):
        return obj.category.name

    def publish_selected(self, request, queryset):
        queryset.update(published=True)

    def unpublish_selected(self, request, queryset):
        queryset.update(published=False)

    def custom_delete_selected(self, request, queryset):
        for obj in queryset:
            obj.delete()

    def delete_model(self, request, obj):
        # Your custom delete_model logic
        # This is just an example, adjust it according to your needs
        obj.delete()



    publish_selected.short_description = "Опубликовать выбранные посты"
    unpublish_selected.short_description = "Снять с публикации выбранные посты"
    custom_delete_selected.short_description = 'Удалить выбранные посты'
    delete_model.short_description = 'Удалить модель'
    category_name.short_description = 'Категория'

