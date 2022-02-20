from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('blog/<slug:slug>/', views.BlogDetailView.as_view(), name='detail'),
    path('write-new-blog/', views.BlogCreateView.as_view(), name='submit'),
    path('submit/success/', views.blog_creation_success, name='submit-success'),
    path('search/<str:query>/', views.SearchBlogsListView.as_view(), name='search'),
    path('nwb/', views.NWBView.as_view(), name='nwb'),
]
