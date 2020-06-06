"""Stage Settings Overrides"""

import os

from django.contrib.messages import constants as message_constants

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ALLOWED_HOSTS = ['*']
DEBUG = False
DEBUG_PROPAGATE_EXCEPTIONS = True
STATICFILES_STORAGE = \
    'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

CUSTOM_MIDDLEWARE = []
CUSTOM_INSTALLED_APPS = []

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

CURRENT_DOMAIN = 'panic-stage.appspot.com'
CURRENT_PROTOCOL = 'https'
ACCOUNT_DEFAULT_HTTP_PROTOCOL = "https"

MESSAGE_LEVEL = message_constants.WARNING

# Control Cookies
REST_COOKIES_SECURE = True
JWT_AUTH_COOKIE_SAMESITE = "Strict"
CSRF_COOKIE_SAMESITE = "Strict"
SESSION_COOKIE_SAMESITE = "Strict"
CSRF_COOKIE_SECURE = True
