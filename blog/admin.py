from django.contrib import admin
from . import models
from mptt.admin import MPTTModelAdmin


# attributes of the post 
@admin.register(models.Post)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', 'status', 'slug', 'author')
    prepopulated_fields = {'slug': ('title',), }


# # attributes of the comment
# @admin.register(models.Comment)
# class CommentAdmin(admin.ModelAdmin):
#     list_display = ("post", "name", "email", "publish", "status")
#     list_filter = ("status","publish")
#     search_fields = ("name","email","content")


# add some categories
admin.site.register(models.Category)


admin.site.register(models.Comment, MPTTModelAdmin)
