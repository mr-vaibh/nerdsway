from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from hitcount.models import HitCount, HitCountMixin

from tinymce.models import HTMLField

from django.template.defaultfilters import slugify
from django.utils.crypto import get_random_string
from django.urls import reverse

from datetime import datetime

# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        return super(Tag, self).save(*args, **kwargs)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Tags'


class Blog(models.Model, HitCountMixin):
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk', related_query_name='hit_count_generic_relation')
    title = models.CharField(max_length=100)
    tags = models.ManyToManyField(Tag, blank=True, related_name='tag')
    slug = models.SlugField(default='', editable=False, max_length=200, null=False, unique=True)
    body = HTMLField()
    excerpt = models.TextField(max_length=500, blank=True)
    show_excerpt_in_blog = models.BooleanField(default=True)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    thumb = models.ImageField(blank=True, upload_to='blog/blog_thumbs')
    thumb_alt = models.CharField(max_length=50, default='', blank=True)

    def __str__(self):
        return self.title

    def snippet(self):
        return self.body[:50] + '...'
    
    def get_datetime(self):
        return datetime.combine(self.date, self.time)

    def get_absolute_url(self):
        kwargs = {
            'pk': self.id,
            'slug': self.slug
        }
        return reverse('blog-detail', kwargs=kwargs)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title + '--' +
                                get_random_string(length=7))
        super(Blog, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-date']


class Comment(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, blank=True, null=True)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='blog')
    name = models.CharField(max_length=50)
    email = models.EmailField()
    body = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-datetime']