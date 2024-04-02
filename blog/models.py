from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class PublishManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Roboczy'
        PUBLISHED = 'PB', 'Opublikowany'

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200,
                            unique_for_date='publish')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='blog_post')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.DRAFT)
    object = models.Manager()
    published = PublishManager()

    # Klasa która odwraca kolejność wpisów
    class Meta:
        ordering = ['-publish']
        # indeksacja w bazie
        indexes = [
            models.Index(fields=['-publish'])
        ]

    def __str__(self):
        return self.title

    # metoda która tworzy kanoniczny adres URL
    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])


class Comment(models.Model):
    nick = models.CharField(max_length=30)
    content = models.CharField(max_length=1000)
    create = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User,
                               null=True,
                               default=None,
                               blank=True,
                               related_name='comments',
                               on_delete=models.CASCADE)
    post = models.ForeignKey(Post,
                             related_name='comments',
                             on_delete=models.CASCADE)
