from django.contrib import admin
from .models import Post, Category, Comment, Author, PostView, Contact


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'created_on')
    list_filter = ("status",)
    search_fields = ['title', 'content']
    #prepopulated_fields = {'slug': ('title',)}


class CategoryAdmin(admin.ModelAdmin):
    pass


class CommentAdmin(admin.ModelAdmin):
    pass


class AuthorAdmin(admin.ModelAdmin):
    pass


admin.site.register(Post, PostAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(PostView)
admin.site.register(Contact)
