from django.http import Http404, HttpResponseNotAllowed
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from hitcount.views import HitCountDetailView
from django.urls import reverse_lazy

from django.contrib.auth.models import User
from .forms import BlogForm

from home.models import SpecialBlog
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

            # Adding Tags
            tags_string = self.request.POST.get('tags', '')
            tags = [x.strip() for x in tags_string.split(',') if x.strip()]

            for tag in tags:
                try:
                    tag_obj = Tag.objects.get(name=tag)
                    form.instance.tags.add(tag_obj)
                except Tag.DoesNotExist:
                    form.instance.tags.create(name=tag)
            
            return self.form_valid(form)


class BlogEditView(UpdateView):
    model = Blog
    form_class = BlogForm
    template_name = 'blog/edit-blog.html'
    context_object_name = 'blog'
    pk_url_kwarg = 'blog_id'

    def post(self, request, *args, **kwargs):
        # Updating Tags (first clearing all tags then adding them each)
        self.get_object().tags.clear()
        tags_string = self.request.POST.get('tags', '')
        tags = [x.strip() for x in tags_string.split(',') if x.strip()]

        for tag in tags:
            try:
                tag_obj = Tag.objects.get(name=tag)
                self.get_object().tags.add(tag_obj)
            except Tag.DoesNotExist:
                self.get_object().tags.create(name=tag)
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('blog:detail',
                            current_app='blog',
                            kwargs={'slug': self.get_object().slug})

class NWBView(ListView):
    model = Blog
    template_name = 'blog/nwb.html'
    context_object_name = 'blogs'

    def get_queryset(self):
        slugs = [blog.slug for blog in SpecialBlog.objects.filter(speciality='nwb')]
        return Blog.objects.filter(slug__in=slugs)

def delete_blog(request, blog_id):
    if not request.user.is_authenticated:
        return redirect(reverse_lazy('account:signin'))
    
    if request.method == 'POST':
        Blog.objects.filter(id=blog_id).delete()
        return redirect(reverse_lazy('account:user_profile', kwargs={'user': request.user}) + '?tab=blogs')
    
    return HttpResponseNotAllowed('Method not allowed')

def comment(request, blog_id):
    blog_object = Blog.objects.get(id=blog_id)

    if request.method == 'POST' and request.user.is_authenticated:
        body = request.POST.get('comment_body', '')    
        Comment.objects.create(user=request.user, blog=blog_object, body=body)

    return redirect(reverse_lazy('blog:detail', kwargs={'slug': blog_object.slug}))