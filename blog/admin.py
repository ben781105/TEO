from django.contrib import admin
from .models import Post,Comment



class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at')
    search_fields = ('title', 'excerpt', 'content')
    list_filter = ('category',)

admin.site.register(Post, PostAdmin)
admin.site.register(Comment)