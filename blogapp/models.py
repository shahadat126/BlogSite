from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class TimeStampMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
        
class Category(TimeStampMixin):
    category_name = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.category_name}"
class Post(TimeStampMixin):
    STATUS_CHOICES = [
        ('draft','DRAFT'),
        ('published','PUBLISHED'),
    ]
    title= models.CharField(max_length=255)
    content= models.TextField()
    category = models.ForeignKey(to=Category,on_delete=models.CASCADE,related_name='posts',null=True,blank=True)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='draft')
    author = models.ForeignKey(to=User,on_delete=models.SET_NULL,null=True,blank=True,related_name='posts')
    
    def __str__(self):
        return self.title
class Comment(TimeStampMixin):
    post= models.ForeignKey(to=Post,on_delete=models.CASCADE)
    author = models.ForeignKey(to=User,on_delete=models.SET_NULL,null=True,blank=True,related_name='comments')
    parents = models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True,related_name='replies')
    body = models.CharField()
    
    def __str__(self):
        return f"{self.author.first_name}-{self.post.title}"