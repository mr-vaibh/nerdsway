from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.syndication.views import Feed
from django.urls import reverse_lazy, reverse

from home.models import Faq, Subscriber, SpecialBlog
from blog.models import Blog, Tag

from config import BRAND_NAME

# Create your views here.

class BlogListView(ListView):
    model = Blog
    template_name = 'home/index.html'
    context_object_name = 'blogs'
    paginate_by = 10

    success_url = reverse_lazy('home:thank_you')
    success_message = 'Thanks for subscribing our newletter, stay tuned!'

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
        slugs = [blog.slug for blog in SpecialBlog.objects.filter(speciality='featured')]
        context['featured_blogs'] = Blog.objects.filter(slug__in=slugs)

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


class RSSBlogFeedView(Feed):
    title = BRAND_NAME
    link = "/blog/"
    description = f"RSS feed of {BRAND_NAME}"
 
    def items(self, user):
        return Blog.objects.all()
 
    def item_title(self, item):
        return item.title
       
    def item_description(self, item):
        from html import unescape
        from django.utils.html import strip_tags
        
        return unescape(strip_tags(item.body))
 
    def item_link(self, item):
       return reverse('blog:detail', args=[item.slug])

class FaqListView(ListView):
    model = Faq
    template_name = 'home/faq.html'
    context_object_name = 'faqs'
    paginate_by = 7

def tag_search(request, query):
    if len(query) > 2:
        data = {
            'suggestions': [tag.name for tag in Tag.objects.filter(name__icontains=query)]
        }
    else:
        data = {'suggestions': []}
    return JsonResponse(data)

def subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('subscribe_email')
        
        if not Subscriber.objects.filter(email=email).exists():
            subscriber = Subscriber(email=email)
            subscriber.save()

        return render(request, 'home/subscribe.html', {'email': email, 'is_submitted': True})
    return render(request, 'home/subscribe.html')


def unsubscribe(request):
    if request.method == 'POST':
        email = request.POST.get('unsubscribe_email')
        Subscriber.objects.filter(email=email).delete()

        return render(request, 'home/unsubscribe.html', {'email': email, 'is_submitted': True})
    return render(request, 'home/unsubscribe.html')