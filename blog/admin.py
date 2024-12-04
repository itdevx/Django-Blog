from django.contrib import admin
from .models import Article, Category


@admin.register(Article)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'status', 'author']
    list_filter = ['title', 'date', 'status']
    prepopulated_fields = {
        'slug': ('title',)
    }


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'category_slug': ('category_name', )
    }
