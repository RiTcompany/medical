from django.contrib import admin

from main_page.models import SocialMedia, MainPage, MainPageVideo, Analysis, Indicator


@admin.register(SocialMedia)
class SocialMediaAdmin(admin.ModelAdmin):
    list_display = ('id', 'icon', 'link')


@admin.register(MainPage)
class MainPageAdmin(admin.ModelAdmin):
    list_display = ('first_btn', 'second_btn', 'third_btn', 'img', 'link')

@admin.register(MainPageVideo)
class MainPageVideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'img', 'link')

@admin.register(Analysis)
class AnalysisAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'name_latin')

@admin.register(Indicator)
class IndicatorAdmin(admin.ModelAdmin):
    autocomplete_fields = ['post']
    list_display = ('id', 'name', 'name_latin', 'category', 'min_value', 'max_value', 'unit', 'post')
