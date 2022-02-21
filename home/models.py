from datetime import date
from django.db import models

# Create your models here.

class Subscriber(models.Model):
    email = models.EmailField(max_length=100, blank=False)
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