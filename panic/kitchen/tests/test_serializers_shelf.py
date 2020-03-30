"""Test the Shelf Serializer."""

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.serializers import ValidationError

from ..models.shelf import Shelf
from ..serializers.shelf import ShelfSerializer


class MockRequest:

  def __init__(self, user):
    self.user = user


class TestShelf(TestCase):

  def sample_shelf(self, user=None, name="Over Sink"):
    """Create a shelf."""
    if user is None:
      user = self.user
    shelf = Shelf.objects.create(user=user, name=name)
    shelf.save()
    self.objects.append(shelf)
    return shelf

  @staticmethod
  def generate_overload(fields):
    return_list = []
    for key, value in fields.items():
      overloaded = dict()
      overloaded[key] = "abc" * value
      return_list.append(overloaded)
    return return_list

  @classmethod
  def setUpTestData(cls):
    cls.objects = list()
    cls.serializer = ShelfSerializer
    cls.fields = {"name": 255}
    cls.user = get_user_model().objects.create_user(
        username="testuser",
        email="test@niallbyrne.ca",
        password="test123",
    )
    cls.request = MockRequest(cls.user)

  def setUp(self):
    self.objects = list()

  def tearDown(self) -> None:
    for obj in self.objects:
      obj.delete()

  def testDeserialize(self):
    test_value = "Refrigerator"
    shelf = self.sample_shelf(self.user, test_value)

    serialized = self.serializer(shelf)

    self.assertDictEqual(serialized.data, {'id': 3, 'name': 'Refrigerator'})

  def testSerialize(self):
    test_value = {"name": "Pantry"}

    serialized = self.serializer(
        context={'request': self.request},
        data=test_value,
    )
    serialized.is_valid(raise_exception=True)
    serialized.save()

    self.assertEqual(serialized.data['name'], test_value['name'])

    query = Shelf.objects.filter(name="Pantry")

    assert len(query) == 1
    self.assertEqual(query[0].user.id, self.user.id)
    self.assertEqual(query[0].name, "Pantry")

  def testFieldLengths(self):
    overloads = self.generate_overload(self.fields)
    for overload in overloads:
      with self.assertRaises(ValidationError):
        serialized = self.serializer(
            context={'request': self.request},
            data=overload,
        )
        serialized.is_valid(raise_exception=True)
