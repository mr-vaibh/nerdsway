from django.contrib import admin

from .models import Blog, Comment, Tag

# Register your models here.

class CommentAdmin(admin.TabularInline):
    model = Comment

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'get_tags', 'date', 'time', 'updated_at', 'views')
    list_filter = ('date', 'updated_at', 'tags',)
    search_fields = ('title', 'body', 'excerpt',)
    inlines = [CommentAdmin]

    def views(self, obj):
        return obj.hit_count.hits
    
    def get_tags(self, obj):
        return "\n".join([tag.name for tag in obj.tags.all()])

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('body', 'blog', 'datetime')

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ('name',)