"""Test the Appengine App Configuration."""

from django.test import TestCase

from ..apps import AppEngineConfig


class TestAppConfig(TestCase):

  def test_config(self):
    assert AppEngineConfig.name == 'appengine'
