"""Authentication and Mixins to Enable Cookie Based JWTs"""

from django.conf import settings
from django.contrib.sessions.middleware import MiddlewareMixin
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from rest_framework_simplejwt.authentication import JWTAuthentication


class JWTCookieAuthentication(JWTAuthentication):
  """Extends the authenticate functionality of :class:`rest_framework_simplejwt
  .authentication.JWTAuthentication`
  """

  def authenticate(self, request):
    """Determines if a request can proceed based on the presence of a valid JWT
    cookie.
    """
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
    """Rewrites the response cookie values to ensure they are handled correctly
    by browsers implementing this standard."""
    csrf_cookie_name = settings.CSRF_COOKIE_NAME
    jwt_auth_cookie = settings.JWT_AUTH_COOKIE
    csrf_cookie_samesite = getattr(settings, "CSRF_COOKIE_SAMESITE", False)
    rest_cookies_secure = getattr(settings, "REST_COOKIES_SECURE", False)
    jwt_auth_cookie_samesite = getattr(
        settings, "JWT_AUTH_COOKIE_SAMESITE", None
    )

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
