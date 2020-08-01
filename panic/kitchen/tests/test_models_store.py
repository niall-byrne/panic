"""Test the Store Model."""

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from ..models.store import Store


class TestStore(TestCase):

  def sample_store(self, user=None, name="No Frills"):
    """Create a test store."""
    if user is None:
      user = self.user
    store = Store.objects.create(user=user, name=name)
    store.save()
    self.objects.append(store)
    return store

  @staticmethod
  def generate_overload(fields):
    return_value = []
    for key, value in fields.items():
      return_value.append({key: "abc" * value})
    return return_value

  @classmethod
  def setUpTestData(cls):
    cls.fields = {"name": 255}
    cls.user = get_user_model().objects.create_user(
        username="testuser",
        email="test@niallbyrne.ca",
        password="test123",
    )

  def setUp(self):
    self.objects = list()

  def tearDown(self) -> None:
    for obj in self.objects:
      obj.delete()

  def testAddStore(self):
    test_name = "Loblaws"
    _ = self.sample_store(self.user, test_name)

    query = Store.objects.filter(name=test_name)

    assert len(query) == 1
    self.assertEqual(query[0].index, test_name.lower())
    self.assertEqual(query[0].name, test_name)
    self.assertEqual(query[0].user.id, self.user.id)

  def testUnique(self):
    test_name = "Loblaws"
    _ = self.sample_store(self.user, test_name)

    with self.assertRaises(ValidationError):
      _ = self.sample_store(self.user, test_name)

    query = Store.objects.filter(name=test_name)
    assert len(query) == 1

  def testAddStoreInjection(self):
    test_name = "Loblaws<script>alert('hi');</script>"
    sanitized_name = "Loblaws&lt;script&gt;alert('hi');&lt;/script&gt;"
    _ = self.sample_store(self.user, test_name)

    query = Store.objects.filter(name=sanitized_name)

    assert len(query) == 1
    self.assertEqual(query[0].name, sanitized_name)
    self.assertEqual(query[0].user.id, self.user.id)

  def testStr(self):
    test_name = "Shoppers Drugmart"
    item = self.sample_store(self.user, test_name)

    self.assertEqual(test_name, str(item))

  def testFieldLengths(self):
    for overloaded_field in self.generate_overload(self.fields):
      local_data = {"name": "Loblaws"}
      local_data.update(overloaded_field)
      with self.assertRaises(ValidationError):
        _ = self.sample_store(**local_data)
