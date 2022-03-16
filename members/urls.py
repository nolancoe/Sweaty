from django.urls import path
from django.contrib.auth import authenticate
from .views import UserRegisterView, AccountSettingsView, PasswordsChangeView, ShowProfilePageView, EditProfilePageView, CreateProfilePageView
from django.contrib.auth import views as auth_views
from . import views



urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),

    path('account_settings/', AccountSettingsView.as_view(), name='account_settings'),
    #path('password/', auth_views.PasswordChangeView.as_view(template_name='registration/change-password.html')),
    path('password/', PasswordsChangeView.as_view(template_name='registration/change-password.html')),
    path('password_success', views.password_success, name="password_success"),
    path('<int:pk>/profile/', ShowProfilePageView.as_view(),name='show_profile_page'),
    path('<int:pk>/edit_profile_page/', EditProfilePageView.as_view(),name='edit_profile_page'),
    path('create_profile_page/', CreateProfilePageView.as_view(),name='create_profile_page'),


]