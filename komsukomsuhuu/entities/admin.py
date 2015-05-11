from django.contrib import admin

# Register your models here.
from .models import Topic, Post


class PostAdmin(admin.ModelAdmin):
    list_display = ['owner', 'topic', 'date_created']


class PostInline(admin.TabularInline):
    model = Post
    extra = 0
    fields = ['owner', 'content', 'date_created']


class TopicAdmin(admin.ModelAdmin):
    inlines = [PostInline]
    list_display = ['group', 'owner', 'date_created']


admin.site.register(Post, PostAdmin)
admin.site.register(Topic, TopicAdmin)