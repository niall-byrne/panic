"""Test wait_for_db admin command."""

from io import StringIO
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase

import kitchen
from ..management.commands.load_testdata import DATA_PRESETS
from ..models.item import Item
from ..models.shelf import Shelf
from ..models.store import Store


class CommandTestInvalid(TestCase):

  def test_invalid_user_specified_stdout(self):
    output_stdout = StringIO()
    output_stderr = StringIO()
    call_command('load_testdata',
                 "non-existent-user",
                 stdout=output_stdout,
                 stderr=output_stderr,
                 no_color=True)

    self.assertIn('The specified user does not exist.',
                  output_stderr.getvalue())
    self.assertEqual(output_stdout.getvalue(), "")


with patch(kitchen.__name__ +
           '.management.commands.load_testdata.DATA_PRESETS') as preset:
  BULK_SIZE = 10
  preset.return_value = DATA_PRESETS.update({'number_of_items': BULK_SIZE})

  class CommandTestValid(TestCase):

    @classmethod
    def setUpTestData(cls):
      cls.output_stdout = StringIO()
      cls.output_stderr = StringIO()
      cls.user = get_user_model().objects.create_user(
          username="created_test_user",
          email="created_test_user@niallbyrne.ca",
          password="test123",
      )
      call_command('load_testdata',
                   cls.user.username,
                   stdout=cls.output_stdout,
                   stderr=cls.output_stderr,
                   no_color=True)

    def setUp(self):
      self.objects = list()

    def tearDown(self):
      for item in Item.objects.filter(user=self.user):
        item.delete()
      for shelf in Shelf.objects.filter(user=self.user):
        shelf.delete()
      for store in Store.objects.filter(user=self.user):
        store.delete()

    def test_valid_user_specified_store_is_valid(self):
      store = Store.objects.filter(user=self.user)
      self.assertEqual(len(store), 1)
      self.assertEqual(store[0].name, DATA_PRESETS['storename'])

    def test_valid_user_specified_shelf_is_valid(self):
      shelf = Shelf.objects.filter(user=self.user)
      self.assertEqual(len(shelf), 1)
      self.assertEqual(shelf[0].name, DATA_PRESETS['shelfname'])

    def test_valid_user_specified_item_is_valid(self):
      store = Store.objects.get(user=self.user)
      shelf = Shelf.objects.get(user=self.user)
      items = Item.objects.filter(user=self.user)
      self.assertEqual(len(items), BULK_SIZE)

      for item in items:
        self.assertEqual(len(item.preferred_stores.all()), 1)
        self.assertEqual(item.preferred_stores.all()[0], store)
        self.assertEqual(item.shelf, shelf)
