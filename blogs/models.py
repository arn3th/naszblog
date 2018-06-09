from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse #użyte do get_absolute_url
from django.utils.text import slugify

# Create your models here.
class Blog(models.Model):
    """Blog użytkownika"""
    title = models.CharField(max_length=200)
    owner = models.ForeignKey(User, related_name='user_blogs',
                               on_delete=models.CASCADE
                              )
    slug = models.SlugField(max_length=250)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('blogs:blog',
                        args=[self.id,
                              self.slug])
    def save(self,force_insert=False, force_update=False, using=None):
        self.slug = slugify(self.title)
        super(Blog,self).save()

class PublicPostManager(models.Manager):
    """Definiuje niestandardowy menedżer do pobierania postów,
        których stan to 'public'."""
    def get_queryset(self):
        return super(PublicPostManager,self).get_queryset()\
                                           .filter(status='public')
#Polega to na wywołaniu metody get_queryset() z filtrem obiektu models.Manager

class Post(models.Model):
    """Post użytkownika na blogu."""
    STATUS_CHOICES = (
                    ('private', 'Prywatny'),
                    ('public', 'Publiczny'),
                    )
    name = models.CharField(max_length=250)
    blog = models.ForeignKey(Blog,related_name='blog_posts',
                               on_delete=models.CASCADE
                              )
    text = RichTextUploadingField(blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=7,
                              choices=STATUS_CHOICES,
                              default='public')
                              
    objects = models.Manager()
    public = PublicPostManager()
    slug = models.SlugField(max_length=250)
                              
    def __str__(self):
        if len(self.text) < 300:
            return self.text
        else:
            return self.text[:300] + "..."
    
    def save(self,force_insert=False, force_update=False, using=None):
        self.slug = slugify(self.name)
        super(Post,self).save()
    
    def get_absolute_url(self):
        return reverse('blogs:post_detail',
                        args=[self.id,
                              self.slug])
        
        
class Comment(models.Model):
    """Komentarz dodany do posta."""
    author = models.ForeignKey(User, related_name='user_comments',
                               on_delete=models.CASCADE
                              )
    post = models.ForeignKey(Post, related_name='post_comments',
                               on_delete=models.CASCADE
                              )
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ('created',)
        
    def __str__(self):
        return self.body

