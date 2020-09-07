from django.contrib import admin
from .models import Article,Comment


# Register your models here.
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title','slug','author','content','image1','image2','image3','publish','created','updated','status']
    prepopulated_fields={'slug':('title',)}
class CommentAdmin(admin.ModelAdmin):
    list_display=['name','email','post','body','created','updated','active']
    list_filter=('updated','created','active')
    search_fields=('name','email','body')


admin.site.register(Article,ArticleAdmin)
admin.site.register(Comment,CommentAdmin)
