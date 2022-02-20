from django.forms import ModelForm, Textarea, CharField
from django.utils.translation import gettext_lazy as _


from tinymce.widgets import TinyMCE
from .models import Blog

class BlogForm(ModelForm):
    body = CharField(widget=TinyMCE())
    
    class Meta:
        model = Blog
        exclude = ['author', 'tags']
        field_requireds = {
            'title': _('Title is required.'),
            'body': _('Body is required.'),
        }
        widgets = {
            'excerpt': Textarea(attrs={'style': 'min-height: unset;height: 180px;'}),
        }