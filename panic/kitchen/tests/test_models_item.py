"""Test the Item Model."""

from datetime import date

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from ..models.item import Item
from ..models.shelf import Shelf
from ..models.store import Store


class TestItem(TestCase):

  # pylint: disable=R0913
  def sample_item(self, user, name, bestbefore, shelf, preferred_stores, price,
                  quantity):
    """Create a test item."""
    if user is None:
      user = self.user
    item = Item.objects.create(name=name,
                               user=user,
                               bestbefore=bestbefore,
                               shelf=shelf,
                               price=price,
                               quantity=quantity)
    item.preferred_stores.add(preferred_stores)
    item.save()
    self.objects.append(item)
    return item

  @staticmethod
  def generate_overload(fields):
    return_value = {}
    for key, value in fields.items():
      return_value[key] = "abc" * value
    return return_value

  @classmethod
  def setUpTestData(cls):
    cls.today = date.today()
    cls.fields = {"name": 255}
    cls.user = get_user_model().objects.create_user(
        username="testuser",
        email="test@niallbyrne.ca",
        password="test123",
    )
    cls.store = Store.objects.create(
        user=cls.user,
        name="No Frills",
    )
    cls.shelf = Shelf.objects.create(
        user=cls.user,
        name="Pantry",
    )
    cls.data = {
        'name': "Canned Beans",
        'bestbefore': cls.today,
        'user': cls.user,
        'shelf': cls.shelf,
        'preferred_stores': cls.store,
        'price': 2.00,
        'quantity': 3
    }

  def setUp(self):
    self.objects = list()

  def tearDown(self) -> None:
    for obj in self.objects:
      obj.delete()

  def testAddItem(self):
    _ = self.sample_item(**self.data)

    query = Item.objects.filter(name=self.data['name'])

    assert len(query) == 1
    item = query[0]
    self.assertEqual(item.name, self.data['name'])
    self.assertEqual(item.bestbefore, self.today)
    self.assertEqual(item.user.id, self.user.id)
    self.assertEqual(item.shelf.id, self.shelf.id)
    self.assertEqual(item.price, self.data['price'])
    self.assertEqual(item.quantity, self.data['quantity'])

  def testAddItemInjection(self):
    injection_attack = dict(self.data)
    injection_attack['name'] = "Canned Beans<script>alert('hi');</script>"
    sanitized_name = "Canned Beans&lt;script&gt;alert('hi');&lt;/script&gt;"

    _ = self.sample_item(**injection_attack)

    query = Item.objects.filter(name=injection_attack['name']).count()
    assert query == 0

    query = Item.objects.filter(name=sanitized_name)
    assert len(query) == 1

    item = query[0]
    self.assertEqual(item.name, sanitized_name)
    self.assertEqual(item.bestbefore, self.today)
    self.assertEqual(item.user.id, self.user.id)
    self.assertEqual(item.shelf.id, self.shelf.id)
    self.assertEqual(item.price, self.data['price'])
    self.assertEqual(item.quantity, self.data['quantity'])

  def testStr(self):
    item = self.sample_item(**self.data)
    self.assertEqual(self.data['name'], str(item))

  def testFieldLengths(self):
    local_data = dict(self.data)
    local_data.update(self.generate_overload(self.fields))
    with self.assertRaises(ValidationError):
      _ = self.sample_item(**local_data)

  def testNegativeQuantity(self):
    item = self.sample_item(**self.data)
    item.quantity = -5
    with self.assertRaises(ValidationError):
      item.save()
