from django.db import models

from django.utils.crypto import get_random_string

# Create your models here.

class Subscriber(models.Model):
    email = models.EmailField(default='', max_length=100, blank=False)
    token = models.CharField(max_length=50, default=get_random_string(length=16), blank=False)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.email

class Faq(models.Model):
    question = models.CharField(max_length=200)
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question

    class Meta:
        ordering = ('-created_at',)