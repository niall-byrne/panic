"""Test the Shelf Model."""

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from ..models.shelf import Shelf


class TestShelf(TestCase):

  def sample_shelf(self, user=None, name="Over Sink"):
    """Create a test shelf."""
    if user is None:
      user = self.user
    shelf = Shelf.objects.create(user=user, name=name)
    shelf.save()
    self.objects.append(shelf)
    return shelf

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

  def testAddShelf(self):
    test_name = "Refrigerator"
    _ = self.sample_shelf(self.user, test_name)

    query = Shelf.objects.filter(name=test_name)

    assert len(query) == 1
    self.assertEqual(query[0].index, test_name.lower())
    self.assertEqual(query[0].name, test_name)
    self.assertEqual(query[0].user.id, self.user.id)

  def testUnique(self):
    test_name = "Above Sink"
    _ = self.sample_shelf(self.user, test_name)

    with self.assertRaises(ValidationError):
      _ = self.sample_shelf(self.user, test_name)

    query = Shelf.objects.filter(name=test_name)
    assert len(query) == 1

  def testAddShelfInjection(self):
    test_name = "Refrigerator<script>alert('hi');</script>"
    sanitized_name = "Refrigerator&lt;script&gt;alert('hi');&lt;/script&gt;"
    _ = self.sample_shelf(self.user, test_name)

    query = Shelf.objects.filter(name=sanitized_name)

    assert len(query) == 1
    self.assertEqual(query[0].index, sanitized_name.lower())
    self.assertEqual(query[0].name, sanitized_name)
    self.assertEqual(query[0].user.id, self.user.id)

  def testStr(self):
    test_name = "Pantry"
    item = self.sample_shelf(self.user, test_name)

    self.assertEqual(test_name, str(item))

  def testFieldLengths(self):
    for overloaded_field in self.generate_overload(self.fields):
      local_data = {"name": "Refrigerator"}
      local_data.update(overloaded_field)
      with self.assertRaises(ValidationError):
        _ = self.sample_shelf(**local_data)
