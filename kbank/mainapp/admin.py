from django.contrib import admin

from .models import Article, Category, Comment, SiteSettings


class CategoryAdmin(admin.ModelAdmin):
    search_fields = ("title",)
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Article)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment)
admin.site.register(SiteSettings)
