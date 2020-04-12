"""Test the Cookie Authentication"""

from unittest.mock import patch

from django.conf import settings
from django.test import TestCase
from django.test.client import RequestFactory

from ..auth import JWTCookieAuthentication


class TestValidCSRF(TestCase):
  """Test the ValidCSRF Permission"""

  def setUp(self) -> None:
    self.factory = RequestFactory()
    self.request = self.factory.get('/fakeEndpoint')
    self.auth = JWTCookieAuthentication()
    self.cookie_name = getattr(settings, 'JWT_AUTH_COOKIE', None)

  def test(self):
    assert True is False
