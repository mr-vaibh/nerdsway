from django.urls import path

from django.views.generic import TemplateView
from . import views

app_name = 'blog'

urlpatterns = [
    path('blog/<slug:slug>/', views.BlogDetailView.as_view(), name='detail'),
    path('blog/edit/<int:blog_id>/', views.BlogEditView.as_view(), name='edit'),
    path('blog/delete/<int:blog_id>/', views.delete_blog, name='delete'),
    path('write-new-blog/', views.BlogCreateView.as_view(), name='submit'),
    path('submit/success/', TemplateView.as_view(template_name='blog/submit-success.html'), name='submit-success'),
    path('search/<str:query>/', views.SearchBlogsListView.as_view(), name='search'),
    path('comment/<int:blog_id>/', views.comment, name='comment'),
    path('nwb/', views.NWBView.as_view(), name='nwb'),
]
