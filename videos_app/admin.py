from django.contrib import admin

from videos_app.models import Video


class VideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'created_at']


admin.site.register(Video, VideoAdmin)
