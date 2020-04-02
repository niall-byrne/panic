"""Test the autosocial management command."""

from io import StringIO
from unittest import mock

from allauth.socialaccount.models import SocialApp
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase

User = get_user_model()


class AutoSocialTestCase(TestCase):

  def __clear_social_accounts(self):
    query = SocialApp.objects.all().filter(provider="google")
    if query is not None:
      for row in query:
        row.delete()

  def setUp(self):
    self.__clear_social_accounts()

  @mock.patch('os.environ.get')
  def test_autoadmin_create(self, environ):

    environ.return_value = "not_very_random_string"

    query = SocialApp.objects.all().filter(provider="google")
    assert len(query) == 0

    output_stdout = StringIO()
    output_stderr = StringIO()
    call_command('autosocial',
                 stdout=output_stdout,
                 stderr=output_stderr,
                 no_color=True)
    assert 'Successfully created social app account.' in output_stdout.getvalue(
    )
    assert output_stderr.getvalue() == ""

    query = SocialApp.objects.get(provider="google")
    assert query.client_id == "not_very_random_string"
    assert query.secret == "not_very_random_string"

  @mock.patch('os.environ.get')
  def test_autoadmin_create_twice(self, environ):

    environ.return_value = "not_very_random_string"

    output_stdout = StringIO()
    output_stderr = StringIO()
    call_command('autosocial',
                 stdout=output_stdout,
                 stderr=output_stderr,
                 no_color=True)

    output_stdout = StringIO()
    output_stderr = StringIO()
    call_command('autosocial',
                 stdout=output_stdout,
                 stderr=output_stderr,
                 no_color=True)
    assert 'The social app already exists.' in output_stdout.getvalue()
    assert output_stderr.getvalue() == ""

    query = SocialApp.objects.get(provider="google")
    assert query.client_id == "not_very_random_string"
    assert query.secret == "not_very_random_string"

    query = SocialApp.objects.all().filter(provider="google")
    assert len(query) == 1

  def tearDown(self):
    self.__clear_social_accounts()
