"""Test the Social Accounts Signal Handlers."""

from unittest import mock

from allauth.account.signals import user_signed_up
from django.contrib.auth import get_user_model
from django.test import TestCase

from .. import signals

User = get_user_model()


class MockProvider:
  account = mock.Mock()


class TestSignals(TestCase):

  def setUp(self):
    self.test_user = "testuser1"
    self.email = "testuser@test.com"

    self.user = User(username=self.test_user, email=self.email)
    self.user.set_password('my password string')
    self.user.save()

  @mock.patch(signals.__name__ + '.process_signup_signal')
  def test_social_signup_google_patch(self, m_handler):

    social_login = MockProvider()
    social_login.account.provider = 'google'
    user_signed_up.send('user_signed_up',
                        user=self.user,
                        request='',
                        sociallogin=social_login)
    m_handler.assert_called()

  def test_social_signup_google_empty_return(self):

    social_login = MockProvider()
    social_login.account.provider = 'google'
    user_signed_up.send('user_signed_up',
                        user=self.user,
                        request='',
                        sociallogin=social_login)

  def tearDown(self):
    if self.user.id:
      self.user.delete()
