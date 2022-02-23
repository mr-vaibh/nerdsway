from django.contrib import admin

from .models import Faq, Subscriber, SpecialBlog

# Register your models here.

@admin.register(SpecialBlog)
class SpecialBlogAdmin(admin.ModelAdmin):
    list_filter = ('speciality',)
    list_display = ('slug', 'speciality')

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'date')

@admin.register(Faq)
class FaqAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer')