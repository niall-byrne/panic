"""Security App Urls"""

from django.urls import path

from .views import CSRFview

app_name = "spa_security"

urlpatterns = [
    path("csrf/", CSRFview.as_view(), name='csrf'),
]
