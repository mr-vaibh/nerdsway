from django.urls import path

from django.contrib.auth import views as auth_views

from . import views

app_name = 'account'
urlpatterns = [
    path('sign-up/', views.sign_up, name='signup'),
    path('sign-in/', auth_views.LoginView.as_view(template_name='account/sign-in.html'), name='signin'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('edit/', views.UserProfileEditView.as_view(), name='user_profile_edit'),
    path('<str:user>/', views.user_profile, name='user_profile'),
]
