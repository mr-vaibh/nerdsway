from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.urls import reverse_lazy

from home.models import Faq, Subscriber
from blog.models import Blog

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


def subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('subscribe_email')
        
        if not Subscriber.objects.filter(email=email).exists():
            subscriber = Subscriber(email=email)
            subscriber.save()

        return render(request, 'home/subscribe.html', {'email': email})
    return redirect(reverse_lazy('home:index'))


def unsubscribe(request):
    if request.method == 'GET':
        email = request.GET.get('subscribe_email')
        
        return render(request, 'home/unsubscribe.html', {'email': email})

    elif request.method == 'POST':
        email = request.POST.get('subscribe_email')
        Subscriber.objects.filter(email=email).delete()

        return render(request, 'home/unsubscribe.html', {'email': email, 'is_submitted': True})

    return redirect(reverse_lazy('home:index'))