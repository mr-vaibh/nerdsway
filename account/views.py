from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import View
from django.views.generic.edit import UpdateView
from django.contrib.auth import logout
from django.contrib.syndication.views import Feed

from django.contrib.auth.models import User
# from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm

from .models import UserProfile
from blog.models import Blog
from .forms import UserProfileEditForm

# Create your views here.

def user_profile(request, user):
    user = get_object_or_404(User, username=user)

    tab = request.GET.get('tab')

    context = {
        'tab': tab,
        'user': user,
        'can_edit': user == request.user,
    }

    if tab == 'blogs':
        blogs = Blog.objects.filter(author=user)
        context['blogs'] = blogs
    return render(request, 'account/user-profile.html', context)


class UserProfileEditView(UpdateView):
    model = UserProfile
    form_class = UserProfileEditForm
    template_name = 'account/user-profile-edit.html'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        if self.request.user.is_authenticated:
            obj = UserProfile.objects.get(user=self.request.user)
            return obj
        else:
            raise Http404('u trynna be funny?')
    
    def get_success_url(self):
        return self.get_redirect_url(self.request.user)
    
    def get_redirect_url(self, user):
        return reverse_lazy('account:user_profile',
                            current_app='account',
                            kwargs={'user': user})


class UserRSSBlogFeedView(Feed):
    title = "Nerdsway"
    link = "/blog/"
    description = "RSS feed of NerdsWay"

    def get_object(self, request, user):
        return User.objects.get(username=user)
 
    def items(self, user):
        return Blog.objects.filter(author=user)
 
    def item_title(self, item):
        return item.title
       
    def item_description(self, item):
        from html import unescape
        from django.utils.html import strip_tags
        
        return unescape(strip_tags(item.body))
 
    def item_link(self, item):
       return reverse('blog:detail', args=[item.slug])

class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def sign_up(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home:index')
    else:
        form = UserCreationForm()
    return render(request, 'account/sign-up.html', {'form': form})