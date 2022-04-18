from django.contrib import admin
from .models import Article, Category


class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Article)
admin.site.register(Category, CategoryAdmin)
