from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from unfold.decorators import display
from .models import Category, Item


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ('id', 'name', 'item_count')
    search_fields = ('name',)
    list_per_page = 20

    # Unfold specific settings
    compressed_fields = True
    list_display_links = ('id', 'name')

    @display(description="Items Count")
    def item_count(self, obj):
        count = obj.items.count()
        if count > 0:
            return format_html(
                '<span style="background: #22c55e; color: white; padding: 4px 12px; border-radius: 12px; font-weight: 500;">{}</span>',
                count
            )
        return format_html(
            '<span style="background: #94a3b8; color: white; padding: 4px 12px; border-radius: 12px; font-weight: 500;">0</span>'
        )


@admin.register(Item)
class ItemAdmin(ModelAdmin):
    list_display = ('id', 'get_image_preview', 'title', 'category', 'has_link', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'caption')
    list_per_page = 20
    readonly_fields = ('created_at', 'updated_at', 'get_image_display')

    # Unfold specific settings
    compressed_fields = True
    list_display_links = ('id', 'title')

    fieldsets = (
        ('Basic Information', {
            'fields': ('category', 'title', 'caption', 'link')
        }),
        ('Image', {
            'fields': ('image', 'get_image_display'),
            'classes': ('tab',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('tab',)
        }),
    )

    @display(description="Preview")
    def get_image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);" />',
                obj.image.url
            )
        return format_html(
            '<div style="width: 50px; height: 50px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 8px; display: flex; align-items: center; justify-content: center; color: white; font-size: 20px;">📷</div>'
        )

    @display(description="Has Link", label=True)
    def has_link(self, obj):
        if obj.link:
            return "Yes", "success"
        return "No", "danger"

    @display(description="Image Display")
    def get_image_display(self, obj):
        if obj.image:
            return format_html(
                '<div style="text-align: center;">'
                '<img src="{}" style="max-width: 500px; width: 100%; height: auto; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.15); margin: 20px 0;" />'
                '<p style="color: #64748b; margin-top: 10px; font-size: 14px;">Image URL: {}</p>'
                '</div>',
                obj.image.url,
                obj.image.url
            )
        return format_html(
            '<div style="padding: 40px; text-align: center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px; color: white;">'
            '<div style="font-size: 48px; margin-bottom: 16px;">📷</div>'
            '<p style="font-size: 18px; font-weight: 500;">No image uploaded</p>'
            '<p style="opacity: 0.8; margin-top: 8px;">Upload an image to see it here</p>'
            '</div>'
        )