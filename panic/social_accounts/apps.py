"""Social Accounts App AppConfig"""

from django.apps import AppConfig


class SocialAccountsConfig(AppConfig):
  name = 'social_accounts'

  def ready(self):
    # pylint: disable=W0611,C0415
    from .signals import social_signup_handler  # noqa: F401
