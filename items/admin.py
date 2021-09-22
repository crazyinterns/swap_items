from django.contrib import admin
from django.utils.html import format_html
from items.models import Category, Item, Image


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = [
        'title',
    ]
    list_display = [
        'title',
    ]


class ImageInline(admin.TabularInline):
    model = Image
    fields = ['img', 'image_preview']
    readonly_fields = ['image_preview']
    extra = 0

    def image_preview(self, obj):
        return format_html("<img src=\"{}\" style=\"max-height: 200px\" />", obj.img.url)


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    raw_id_fields = [
        'items_to_swap'
    ]
    search_fields = ['title']
    list_display = [
        'title',
        'created_at',
        'owner'
    ]
    inlines = [ImageInline]


