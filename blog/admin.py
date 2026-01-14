from django.contrib import admin
from .models import Post, Comment
# Register your models here.

# admin.site.register(Post)
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'published_date', 'status']
    list_filter = ['status', 'created_date', 'published_date', 'author']
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']
    date_hierarchy = 'published_date'
    ordering = ['status', 'published_date']
    show_facets = admin.ShowFacets.ALWAYS

@admin.register(Comment)
class CommntAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'created_date', 'active']
    list_filter = ['active', 'created_date', 'updated_date']
    search_fields = ['name', 'email', 'body']
    
    