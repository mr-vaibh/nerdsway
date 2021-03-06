from cProfile import label
from django.forms import ModelForm, Textarea, CharField
from django.utils.translation import gettext_lazy as _


from tinymce.widgets import TinyMCE
from .models import Blog, Comment

class BlogForm(ModelForm):
    body = CharField(widget=TinyMCE(), label='Write your blog, (fullscreen mode available)')

    class Meta:
        model = Blog
        exclude = ['author', 'tags']
        field_requireds = {
            'title': _('Title is required.'),
            'body': _('Body is required.'),
        }
        labels = {
            'thumb' : 'Thumbnail',
            'thumb_alt': 'Thumbnail Description (optional)',
        }
        widgets = {
            'excerpt': Textarea(attrs={'style': 'min-height: unset;height: 180px;'}),
        }