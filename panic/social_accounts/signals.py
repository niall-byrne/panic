"""Signal Handlers for the Social Accounts App"""

from allauth.account.signals import user_signed_up
from django.dispatch import receiver


# pylint: disable=W0613,W0201
@receiver(user_signed_up)
def social_signup_handler(request, user, sociallogin=None, **kwargs):
  """A signal handler that is triggered when a
    :class:`user_accounts.models.CustomUser` model is created through a social
    signup.

    The handler is here future integrations.

    :param request: The instance that was saved.
    :type request: :class:`django.http.HttpRequest`
    :param user: The new User object.
    :type user: :class:`django.http.HttpRequest`
    :param sociallogin: The social login created by Django Allauth.
    :type sociallogin: :class:`allauth.socialaccount.models.SocialLogin`
    """
  process_signup_signal(request, user, sociallogin=None, **kwargs)


def process_signup_signal(request, user, sociallogin=None, **kwargs):
  return
