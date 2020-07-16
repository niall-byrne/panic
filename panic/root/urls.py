"""panic URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from allauth.socialaccount.views import connections, signup
from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

urlpatterns = [
    path("", include("appengine.urls")),
    path("api/v1/", include("kitchen.urls")),
    path("api/v1/auth/", include('dj_rest_auth.urls')),
    path("api/v1/auth/registration/",
         include('dj_rest_auth.registration.urls')),
    path("api/v1/auth/", include("spa_security.urls")),
    path("api/v1/auth/social/", include("social_accounts.urls")),
    path("api/v1/auth/social/signup/", signup, name='socialaccount_signup'),
    path("api/v1/auth/social/connect/",
         connections,
         name='socialaccount_connections'),
    path('watchman/', include("watchman.urls")),
]

if settings.ENVIRONMENT in ['local', 'stage', 'admin']:
  urlpatterns = [path('admin/', admin.site.urls)] + urlpatterns

  SchemaView = get_schema_view(
      openapi.Info(
          title="Don't Panic API!",
          default_version='v1',
          description="A Pandemic Kitchen Inventory Manager",
          terms_of_service="https://www.google.com/policies/terms/",
          contact=openapi.Contact(email="niall@niallbyrne.ca"),
          license=openapi.License(name="MPL 2.0 License"),
      ),
      public=True,
      permission_classes=(permissions.AllowAny,),
  )

  urlpatterns += [
      url(r'^swagger(?P<format>\.json|\.yaml)$',
          SchemaView.without_ui(cache_timeout=0),
          name='schema-json'),
      url(r'^swagger/$',
          SchemaView.with_ui('swagger', cache_timeout=0),
          name='schema-swagger-ui'),
  ]
