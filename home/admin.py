from django.contrib import admin
from .models import Categories

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'category_slug': ('category_name',)}
    list_display = ('category_name', 'category_slug','category_image')
    list_editable = ('category_slug','category_image')  # Make 'category_slug' editable instead
    list_display_links = ('category_name',)  # Set 'category_name' as a link

admin.site.register(Categories, CategoryAdmin)
