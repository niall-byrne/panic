"""Test the Store Serializer."""

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.serializers import ValidationError

from ..models.store import Store
from ..serializers import DUPLICATE_OBJECT_MESSAGE
from ..serializers.store import StoreSerializer


class MockRequest:

  def __init__(self, user):
    self.user = user


class TestStore(TestCase):

  def sample_store(self, user=None, name="No Frills"):
    """Create a store."""
    if user is None:
      user = self.user
    store = Store.objects.create(user=user, name=name)
    store.save()
    self.objects.append(store)
    return store

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
    cls.serializer = StoreSerializer
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
    test_value = "Loblaws"
    store = self.sample_store(self.user, test_value)

    serialized = self.serializer(store)
    self.assertEqual(serialized.data['name'], test_value)

  def testSerialize(self):
    test_value = {"name": "Super Store"}

    serialized = self.serializer(
        context={'request': self.request},
        data=test_value,
    )
    serialized.is_valid(raise_exception=True)
    serialized.save()

    self.assertEqual(serialized.data['name'], test_value['name'])

    query = Store.objects.filter(name=test_value['name'])

    assert len(query) == 1
    self.assertEqual(query[0].user.id, self.user.id)
    self.assertEqual(query[0].name, test_value['name'])

  def testUniqueConstraint(self):
    test_value = {"name": "Super Store"}

    serialized = self.serializer(
        context={'request': self.request},
        data=test_value,
    )
    serialized.is_valid(raise_exception=True)
    serialized.save()

    serialized2 = self.serializer(
        context={'request': self.request},
        data=test_value,
    )
    with self.assertRaises(ValidationError):
      serialized2.is_valid(raise_exception=True)

    self.assertEqual(
        str(serialized2.errors['non_field_errors'][0]), DUPLICATE_OBJECT_MESSAGE
    )

  def testFieldLengths(self):
    overloads = self.generate_overload(self.fields)
    for overload in overloads:
      with self.assertRaises(ValidationError):
        serialized = self.serializer(
            context={'request': self.request},
            data=overload,
        )
        serialized.is_valid(raise_exception=True)
