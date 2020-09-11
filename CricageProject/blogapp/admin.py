from django.contrib import admin
from .models import Article,Comment,AcademyUser


# Register your models here.
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title','slug','author','content','image1','image2','image3','publish','created','status','type']
    prepopulated_fields={'slug':('title',)}

class CommentAdmin(admin.ModelAdmin):
    list_display=['name','email','post','body','created','updated','active']
    list_filter=('updated','created','active')
    search_fields=('name','email','body')

class AcademyUserAdmin(admin.ModelAdmin):
    list_display=['first_name','last_name','email','phone_no']


admin.site.register(Article,ArticleAdmin)
admin.site.register(Comment,CommentAdmin)
admin.site.register(AcademyUser,AcademyUserAdmin)
