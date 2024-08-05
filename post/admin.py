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
    list_display = ('name', 'main_post')
    exclude = ('slug',)
    search_fields = ['name', 'slug', 'main_post']
    
    list_filter = (NameStartsWithFilter,)
    
    def custom_delete_selected(self, request, queryset):
        for obj in queryset:
            obj.delete()

    custom_delete_selected.short_description = 'Удалить выбранные категории'

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category_name', 'create_at',
                    'update_at', 'published', 'position_in_category')
    search_fields = ['id', 'name', 'category__name']
    list_filter = [('category', RelatedOnlyDropdownFilter), 'published']
    

    actions = ['delete_model', 'publish_selected', 'unpublish_selected']

    def category_name(self, obj):
        return obj.category.name

    def publish_selected(self, request, queryset):
        queryset.update(published=True)

    def unpublish_selected(self, request, queryset):
        queryset.update(published=False)

    def get_actions(self, request):
        actions = super(PostAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def delete_model(self, request, obj):
        for o in obj.all():
            o.delete()

    publish_selected.short_description = "Опубликовать выбранные посты"
    unpublish_selected.short_description = "Снять с публикации выбранные посты"
    delete_model.short_description = 'Удалить выбранные посты'
    category_name.short_description = 'Категория'

