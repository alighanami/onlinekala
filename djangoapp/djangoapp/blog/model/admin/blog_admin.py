from django.contrib import admin

from blog.model.blog import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title','created_at','is_published','updated_at','visit_count',)
    list_filter = ('created_at','is_published','updated_at',)
    search_fields = ('title','content')
    list_editable = ('is_published',)