"""Shared Shelf Test Fixtures for Kitchen"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from ...models.shelf import Shelf
from .abc_model_fixture import KitchenModelTestFixture


class ShelfTestHarness(KitchenModelTestFixture, TestCase):
  user1 = None
  user2 = None
  objects = None

  @staticmethod
  def create_instance(**kwargs):
    """Create a test shelf."""
    shelf = Shelf.objects.create(user=kwargs['user'], name=kwargs['name'])
    shelf.save()
    return shelf

  @staticmethod
  def create_dependencies(seed):
    user = get_user_model().objects.create_user(
        username=f"testuser{seed}",
        email=f"test{seed}@niallbyrne.ca",
        password="test123",
    )

    return {
        "user": user,
    }

  @classmethod
  def create_data_hook(cls):
    pass

  def create_test_instance(self, **kwargs):
    """Create a test shelf."""
    shelf = self.__class__.create_instance(**kwargs)
    self.objects.append(shelf)
    return shelf

  def create_second_test_set(self):
    test_data1 = self.__class__.create_dependencies(2)
    self.user2 = test_data1['user']
    self.objects = self.objects + [self.user2]

  @classmethod
  def setUpTestData(cls):
    cls.today = timezone.now()
    test_data1 = cls.create_dependencies(1)
    cls.user1 = test_data1['user']
    cls.create_data_hook()

  def setUp(self):
    self.objects = list()

  def tearDown(self):
    for obj in self.objects:
      obj.delete()
