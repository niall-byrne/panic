"""Django Automated Social App Creation."""
import os

from allauth.socialaccount.models import SocialApp
from django.core.management.base import BaseCommand


class Command(BaseCommand):
  """Bootstraps the Social Authentication by populating social logins based on
  environment variables.

  - Generate Social Login Authorization::

    ./manage.py autosocial

  - Credentials:
    client_id: ENV -> GOOGLE_CLIENT_ID
    secret:    ENV -> GOOGLE_CLIENT_KEY
 """
  help = 'Adds social app configuration without user interaction.'

  def handle(self, *args, **options):

    query = SocialApp.objects.all().filter(provider='google').count()
    if query > 0:
      self.stdout.write(self.style.ERROR('The social app already exists.'))
    else:

      social_app = SocialApp(provider='google',
                             name='playcounts3',
                             client_id=os.getenv('GOOGLE_CLIENT_ID', ''),
                             secret=os.getenv('GOOGLE_CLIENT_KEY', ''))

      social_app.save()
      social_app.sites.add(1)

      self.stdout.write(
          self.style.SUCCESS('Successfully created social app account.'))
