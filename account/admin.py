from django.contrib import admin
from django.utils.html import format_html
from .models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html('<img src="{}" width="40" style="border-radius:40%;">'.format(object.profile_picture.url))
    thumbnail.short_description = 'Profile Picture'
    list_display = ('thumbnail', 'user','email', 'city', 'state', 'country')

admin.site.register(UserProfile,UserProfileAdmin)
