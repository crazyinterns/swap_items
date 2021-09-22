from django.contrib import admin
from items.models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = [
        'title',
    ]
    list_display = [
        'title',
    ]
