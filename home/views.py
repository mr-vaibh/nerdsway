from django.shortcuts import render
from django.views.generic import ListView

from home.models import Faq
from blog.models import Blog

# Create your views here.

class BlogListView(ListView):
    model = Blog
    template_name = 'home/index.html'
    context_object_name = 'blogs'
    paginate_by = 10

    def get_queryset(self):
        # Call the base implementation first to get a context
        blogs = super(BlogListView, self).get_queryset()
        # Add extras
        blogs = blogs[:108]
        return blogs

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(BlogListView, self).get_context_data(**kwargs)
        # Add extras
        context['featured_blogs'] = Blog.objects.filter(tags__name__in=['featured'])[:3]

        return context


class TagListView(ListView):
    model = Blog
    template_name = 'home/tag.html'
    context_object_name = 'blogs'
    paginate_by = 12

    def get_queryset(self):
        # Call the base implementation first to get a context
        blogs = super(TagListView, self).get_queryset()
        # Add extras
        tag = self.kwargs['tag']
        blogs = blogs.filter(tags__name__in=[tag])[:108]
        return blogs

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(TagListView, self).get_context_data(**kwargs)
        # Add extras
        context['tag'] = self.kwargs['tag']
        return context


class FaqListView(ListView):
    model = Faq
    template_name = 'home/faq.html'
    context_object_name = 'faqs'
    paginate_by = 7