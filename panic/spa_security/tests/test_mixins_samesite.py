"""Test SameSite Cookie Middleware"""

from django.conf import settings
from django.http import HttpResponse
from django.test import TestCase, override_settings

from ..auth_cookie import SameSiteMiddleware


class TestSameSiteMiddleware(TestCase):

  def setUp(self) -> None:
    self.response = HttpResponse()

  @override_settings(CSRF_COOKIE_SAMESITE=None)
  def test_csrf_cookie_same_site_none(self):
    cookie_name = settings.CSRF_COOKIE_NAME
    self.response.set_cookie(cookie_name, "somevalue")
    SameSiteMiddleware.process_response(None, None, self.response)
    self.assertEqual(self.response.cookies[cookie_name]['samesite'], 'None')

  @override_settings(CSRF_COOKIE_SAMESITE="lax")
  def test_csrf_cookie_same_site_lax(self):
    cookie_name = settings.CSRF_COOKIE_NAME
    self.response.set_cookie(cookie_name, "somevalue")
    SameSiteMiddleware.process_response(None, None, self.response)
    self.assertNotEqual(self.response.cookies[cookie_name]['samesite'], 'None')

  @override_settings(REST_COOKIES_SECURE=False)
  def test_csrf_cookie_same_site_not_secure(self):
    cookie_name = settings.CSRF_COOKIE_NAME
    self.response.set_cookie(cookie_name, "somevalue")
    SameSiteMiddleware.process_response(None, None, self.response)
    self.assertFalse(self.response.cookies[cookie_name]['secure'])

  @override_settings(REST_COOKIES_SECURE=True)
  def test_csrf_cookie_same_site_secure(self):
    cookie_name = settings.CSRF_COOKIE_NAME
    self.response.set_cookie(cookie_name, "somevalue")
    SameSiteMiddleware.process_response(None, None, self.response)
    self.assertTrue(self.response.cookies[cookie_name]['secure'])

  @override_settings(JWT_AUTH_COOKIE_SAMESITE="lax")
  def test_jwt_cookie_same_site_lax(self):
    cookie_name = settings.JWT_AUTH_COOKIE
    self.response.set_cookie(cookie_name, "somevalue")
    SameSiteMiddleware.process_response(None, None, self.response)
    self.assertEqual(self.response.cookies[cookie_name]['samesite'], 'lax')

  @override_settings(JWT_AUTH_COOKIE_SAMESITE=None)
  def test_jwt_cookie_same_site_none(self):
    cookie_name = settings.JWT_AUTH_COOKIE
    self.response.set_cookie(cookie_name, "somevalue")
    SameSiteMiddleware.process_response(None, None, self.response)
    self.assertEqual(self.response.cookies[cookie_name]['samesite'], 'None')

  @override_settings(REST_COOKIES_SECURE=False)
  def test_jwt_cookie_same_site_not_secure(self):
    cookie_name = settings.JWT_AUTH_COOKIE
    self.response.set_cookie(cookie_name, "somevalue")
    SameSiteMiddleware.process_response(None, None, self.response)
    self.assertFalse(self.response.cookies[cookie_name]['secure'])

  @override_settings(REST_COOKIES_SECURE=True)
  def test_jwt_cookie_same_site_secure(self):
    cookie_name = settings.JWT_AUTH_COOKIE
    self.response.set_cookie(cookie_name, "somevalue")
    SameSiteMiddleware.process_response(None, None, self.response)
    self.assertTrue(self.response.cookies[cookie_name]['secure'])

  def tearDown(self):
    pass
