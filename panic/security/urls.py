"""Url Patterns for the Social Accounts App"""

from django.urls import path
from .views import CSRFview

app_name = "security"

urlpatterns = [
    path("csrf/", CSRFview.as_view(), name='csrf'),
]
