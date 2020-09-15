from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone



# Create your models here.
class Article(models.Model):
    STATUS_CHOICES=(('draft','Draft'),('published','Published'))
    title=models.CharField(max_length=256)
    slug=models.SlugField(max_length=264,unique_for_date='publish')
    author=models.ForeignKey(User,related_name='blog_articles',on_delete = models.CASCADE)
    content=models.TextField()
    image1=models.ImageField(upload_to='images/',blank=True)
    image2=models.ImageField(upload_to='images/',blank=True)
    image3=models.ImageField(upload_to='images/',blank=True)
    image4=models.ImageField(upload_to='images/',blank=True)
    image5=models.ImageField(upload_to='images/',blank=True)
    image6=models.ImageField(upload_to='images/',blank=True)
    publish=models.DateTimeField(default=timezone.now)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    status=models.CharField(max_length=10,choices=STATUS_CHOICES,default='draft')
    type=models.CharField(max_length=20,default='news')

    class Meta:
        ordering=('-publish',)

    def __str__(self):
        return self.title

class Comment(models.Model):
    post=models.ForeignKey(Article,related_name='comments',on_delete = models.CASCADE)
    name=models.CharField(max_length=32)
    email=models.EmailField()
    body=models.TextField()
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    active= models.BooleanField(default=True)
    class Meta:
        ordering=('-created',)

    def __str__(self):
        return self.name

class AcademyUser(models.Model):
    first_name=models.CharField(max_length=12)
    last_name=models.CharField(max_length=12)
    email=models.EmailField()
    phone_no=models.CharField(max_length=10)
