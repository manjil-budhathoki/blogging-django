from django.db import models
from django.utils import timezone
from django.conf import settings
from django.urls import reverse

# Create your models here.
class PublisedManager(models.Manager):

    def get_queryset(self):
        return (
            super().get_queryset().filter(status=Post.Status.PUBLISHED)
        )

class Post(models.Model):

    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='published_date')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,# using CASCADE to delete posts if user is deleted
        related_name='blog_posts'
    )
    body = models.TextField()

    published_date = models.DateTimeField(default=timezone.now)

    '''
    auto_now - updates the value of field to current time and date every time the model.save() is called.

    auto_now_add - updates the value with the time and date of creation of record.
    '''
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.DRAFT
    )
    objects = models.Manager() # The default manager.
    published = PublisedManager() # Our custom manager.

    class Meta:
        ordering = ['-published_date']
        indexes = [
            models.Index(fields=['-published_date']),
        ]

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse(
            'blog:post_detail',
            args=[
                self.published_date.year,
                self.published_date.month,
                self.published_date.day,
                self.slug
            ]
        )
    
class Comment(models.Model):
        post = models.ForeignKey(
            Post,
            on_delete=models.CASCADE,
            related_name='comments'
        )
        name = models.CharField(max_length=80)
        email = models.EmailField()

        body = models.TextField()

        created_date = models.DateTimeField(auto_now_add=True)
        updated_date = models.DateTimeField(auto_now=True)
        active = models.BooleanField(default=True) # to moderate comments

        class Meta:
            ordering = ['created_date']
            indexes = [
                models.Index(fields=['created_date']),
            ]
        def __str__(self):
            return f'Comment by {self.name} on {self.post}'
    

