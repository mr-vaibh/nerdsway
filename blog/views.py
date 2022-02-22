from ctypes import Union
from django.shortcuts import render
from django.views.generic import ListView, CreateView
from django.contrib.messages.views import SuccessMessageMixin
from hitcount.views import HitCountDetailView
from django.urls import reverse_lazy

from django.contrib.auth.models import User
from .forms import BlogForm

from .models import Blog, Comment, Tag


class BlogDetailView(HitCountDetailView):
    model = Blog
    template_name = 'blog/single-standard.html'
    context_object_name = 'blog'
    count_hit = True
    
    def get_context_data(self, **kwargs):
        context = super(BlogDetailView, self).get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(blog=self.get_object())
        return context
        

class SearchBlogsListView(ListView):
    model = Blog
    template_name = 'blog/search-blogs.html'
    paginate_by = 10
    context_object_name = 'blogs'
    
    def get_queryset(self):
        blogs = super(SearchBlogsListView, self).get_queryset()
        params = {
            'query': self.kwargs.get('query'),
            'sort_by': self.request.GET.get('sort_by'),
            'date_from': self.request.GET.get('date_from'),
            'date_to': self.request.GET.get('date_to'),
        }
        blogs = Blog.objects.search(**params)
        
        return blogs
    
    def get_context_data(self, **kwargs):
        context = super(SearchBlogsListView, self).get_context_data(**kwargs)
        context['query'] = self.kwargs.get('query', None)
        context['filters'] = {
            'sort_by': self.request.GET.get('sort_by', ''),
            'date_from': self.request.GET.get('date_from', ''),
            'date_to': self.request.GET.get('date_to', ''),
        }
        return context

class BlogCreateView(SuccessMessageMixin, CreateView):
    model = Blog
    form_class = BlogForm
    template_name = 'blog/submit-blog.html'
    context_object_name = 'blog'
    success_url = reverse_lazy('blog:submit-success')
    success_message = 'Your blog has been created successfully'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.instance.author = User.objects.get(username=request.user)
            form.instance.save()

            tags = self.request.POST.get('tags', []).split(',')

            if 'featured' in tags:
                tags.remove('featured')
            if 'nwb' in tags:
                tags.remove('nwb')

            for tag in tags:
                if tag.strip():
                    try:
                        tag_obj = Tag.objects.get(name=tag.strip())
                        form.instance.tags.add(tag_obj)
                    except Tag.DoesNotExist:
                        form.instance.tags.create(name=tag.strip())
            
            # Mailing feature
            from django.core.mail import EmailMultiAlternatives
            from django.template.loader import render_to_string
            from html import unescape
            from django.utils.html import strip_tags
            from home.models import Subscriber

            mailing_list = [email for email in Subscriber.objects.values_list('email', flat=True)]

            html_content = render_to_string('account/email_template.html', {'title': form.instance.title, 'content': unescape(form.instance.body)})
            text_content = strip_tags(html_content)

            email = EmailMultiAlternatives(
                form.instance.title,
                text_content,
                '',
                mailing_list,
            )
            email.attach_alternative(html_content, "text/html")
            email.send()
            
            return self.form_valid(form)

class NWBView(ListView):
    model = Blog
    template_name = 'blog/nwb.html'
    context_object_name = 'blogs'

    def get_queryset(self):
        blogs = super(NWBView, self).get_queryset()
        blogs = blogs.filter(tags__name='nwb').order_by('-date')
        return blogs


def blog_creation_success(request):
    return render(request, 'blog/submit-success.html')
def blog(request):
    return render(request, 'blog/blog.html')