from django.contrib import admin
from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish', 'status']
    list_filter = ['status', 'create', 'publish', 'author']
    search_fields = ['title', 'body']
    # linijka która tworzy slug automatycznie na podstawie title
    prepopulated_fields = {'slug': ('title',)}
    # autor wyszukiwany po kluczu głównym w swojej tabeli
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['content', 'nick', 'create', 'author', 'post']
    list_filter = ['nick', 'author', 'post', 'create']
    search_fields = ['nick', 'content']
    raw_id_fields = ['author', 'post']
    ordering = ['create']
