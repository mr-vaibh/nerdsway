from django import template
from django.utils.safestring import mark_safe

from config import BRAND_NAME

register = template.Library()

@register.simple_tag
def robots(index=False, follow=False):
    content = 'noindex, nofollow'
    
    if index and not follow:
        content = 'nofollow'
    elif not index and follow:
        content = 'noindex'
    elif index and follow:
        content = ''
    
    return mark_safe(f'<meta name="robots" content="{content}">')

@register.simple_tag
def brand_name():
    return BRAND_NAME