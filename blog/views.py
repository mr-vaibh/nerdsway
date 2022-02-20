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
        query = self.kwargs.get('query', None)
        blogs = Blog.objects.filter(title__icontains=query)

        sort_by = self.request.GET.get('sort_by', '')
        date_from = self.request.GET.get('date_from', '')
        date_to = self.request.GET.get('date_to', '')

        if sort_by == 'popular':
            blogs = blogs.order_by('-hit_count_generic__hits')
        elif sort_by == 'newest':
            blogs = blogs.order_by('-date')
        elif sort_by == 'oldest':
            blogs = blogs.order_by('date')
        
        if date_from and date_to:
            blogs = blogs.filter(date__range=(date_from, date_to))
        
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
    success_message = 'Your blog request has been submitted successfully'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.instance.author = User.objects.get(username=request.user)
            form.instance.save()

            tags = self.request.POST.get('tags', []).split(',')

            tags.remove('featured')

            for tag in tags:
                try:
                    tag_obj = Tag.objects.get(name=tag)
                    form.instance.tags.add(tag_obj)
                except Tag.DoesNotExist:
                    form.instance.tags.create(name=tag)
                
            return self.form_valid(form)

class BlogView(ListView):
    model = Blog
    template_name = 'blog/blog.html'
    context_object_name = 'blogs'

    def get_queryset(self):
        blogs = super(BlogView, self).get_queryset()
        blogs = blogs.filter(tags__name='blog').order_by('-date')
        return blogs


def blog_creation_success(request):
    return render(request, 'blog/submit-success.html')
def blog(request):
    return render(request, 'blog/blog.html')