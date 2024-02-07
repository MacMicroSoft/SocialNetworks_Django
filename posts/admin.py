from django.contrib import admin

from .models import Tags, Images, Posts


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = ('id', 'tags')


@admin.register(Images)
class ImagesAdmin(admin.ModelAdmin):
    list_display = ('id', 'image')


@admin.register(Posts)
class PostsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'comments', 'date')
    list_filter = ('date',)
    raw_id_fields = ('tags', 'like', 'images')
