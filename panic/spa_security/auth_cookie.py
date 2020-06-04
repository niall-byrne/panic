"""Authentication and Mixins to Enable Cookie Based JWTs"""

from django.conf import settings
from django.contrib.sessions.middleware import MiddlewareMixin
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from rest_framework_simplejwt.authentication import JWTAuthentication


class JWTCookieAuthentication(JWTAuthentication):
  """The library implementation of this method would fail on a mangled header,
  skipping the cookie check altogether.  I've pulled out the header checks,
  this now strictly checks for the presence of a named cookie.

  This makes auth reliable, even in the presence of header mangling extensions.
  """

  def authenticate(self, request):
    cookie_name = getattr(settings, 'JWT_AUTH_COOKIE', None)
    raw_token = None

    if cookie_name:
      if cookie_name in request.COOKIES:
        raw_token = request.COOKIES.get(cookie_name)

    if not raw_token:
      return None

    validated_token = self.get_validated_token(raw_token)
    return self.get_user(validated_token), validated_token


class SameSiteMiddleware(MiddlewareMixin):
  """Comply with the latest standard for samesite cookies."""

  def process_response(self, request, response):
    csrf_cookie_name = settings.CSRF_COOKIE_NAME
    jwt_auth_cookie = settings.JWT_AUTH_COOKIE
    csrf_cookie_samesite = getattr(settings, "CSRF_COOKIE_SAMESITE", False)
    rest_cookies_secure = getattr(settings, "REST_COOKIES_SECURE", False)
    jwt_auth_cookie_samesite = getattr(settings, "JWT_AUTH_COOKIE_SAMESITE",
                                       None)

    if csrf_cookie_name in response.cookies:
      if csrf_cookie_samesite is None:
        response.cookies[csrf_cookie_name]['samesite'] = 'None'
      if rest_cookies_secure:
        response.cookies[csrf_cookie_name]['secure'] = True
    if jwt_auth_cookie in response.cookies:
      if jwt_auth_cookie_samesite is None:
        response.cookies[jwt_auth_cookie]['samesite'] = 'None'
      else:
        response.cookies[jwt_auth_cookie]['samesite'] = jwt_auth_cookie_samesite
      if rest_cookies_secure:
        response.cookies[jwt_auth_cookie]['secure'] = True
    return response


class CSRFMixin:
  """Ensures the endpoint performs CSRF validation, or returns an error."""

  @method_decorator(csrf_protect)
  def dispatch(self, *args, **kwargs):
    return super(CSRFMixin, self).dispatch(*args, **kwargs)
