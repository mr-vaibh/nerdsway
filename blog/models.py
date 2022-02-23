from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from hitcount.models import HitCount, HitCountMixin

from django.dispatch import receiver
from django.db.models.signals import post_save

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


class BlogQuerySet(models.QuerySet):
    def search(self, **kwargs):
        queryset = self

        search_query = kwargs.get('query', None)
        queryset = (queryset.filter(title__icontains=search_query) | queryset.filter(body__icontains=search_query) | queryset.filter(tags__name__in=[search_query]))

        sort_by = kwargs.get('sort_by', '')
        date_from = kwargs.get('date_from', '')
        date_to = kwargs.get('date_to', '')

        if sort_by == 'popular':
            queryset = queryset.order_by('-hit_count_generic__hits')
        elif sort_by == 'newest':
            queryset = queryset.order_by('-date')
        elif sort_by == 'oldest':
            queryset = queryset.order_by('date')
        
        if date_from and date_to:
            queryset = queryset.filter(date__range=(date_from, date_to))
        return queryset

class Blog(models.Model, HitCountMixin):
    objects = BlogQuerySet.as_manager()

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
    
    def get_read_time(self):
        from html import unescape
        from django.utils.html import strip_tags
        
        string = self.title + unescape(strip_tags(self.body))
        total_words = len((string).split())

        return round(total_words / 200)

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title + '--' +
                                get_random_string(length=7))
        for field_name in ['title', 'excerpt']:
            val = getattr(self, field_name, False)
            if val:
                setattr(self, field_name, val.capitalize())
        super(Blog, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-date']

@receiver(post_save, sender=Blog)
def send_newsletter(sender, instance, created, **kwargs):
    if created:
        from django.core.mail import EmailMultiAlternatives
        from django.template.loader import render_to_string
        from html import unescape
        from django.utils.html import strip_tags
        from home.models import Subscriber

        mailing_list = [email for email in Subscriber.objects.values_list('email', flat=True)]

        html_content = render_to_string('account/email_template.html', {
            'title': instance.title,
            'content': unescape(instance.body),
        })
        text_content = strip_tags(html_content)

        email = EmailMultiAlternatives(
            instance.title,
            text_content,
            '',
            mailing_list,
        )
        email.attach_alternative(html_content, "text/html")
        email.send()

class Comment(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, blank=False)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='blog')
    body = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[:50]

    class Meta:
        ordering = ['-datetime']