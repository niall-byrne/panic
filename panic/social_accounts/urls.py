"""Url Patterns for the Social Accounts App"""

from allauth.socialaccount.views import signup
from django.urls import path

from .social import FacebookLogin, GoogleLogin

urlpatterns = [
    path("facebook/", FacebookLogin.as_view(), name='fb_login'),
    path("google/", GoogleLogin.as_view(), name='google_login'),
    path("signup/", signup, name='socialaccount_signup'),
]
