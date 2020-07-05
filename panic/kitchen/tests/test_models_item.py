"""Test the Item Model."""

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from ..models.item import (
    MAXIMUM_QUANTITY,
    MAXIMUM_SHELF_LIFE,
    MINIMUM_QUANTITY,
    MINIMUM_SHELF_LIFE,
    Item,
)
from ..models.shelf import Shelf
from ..models.store import Store


class TestItem(TestCase):

  # pylint: disable=R0913
  def sample_item(self, user, name, shelf_life, shelf, preferred_stores, price,
                  quantity):
    """Create a test item."""
    if user is None:
      user = self.user
    item = Item.objects.create(name=name,
                               user=user,
                               shelf_life=shelf_life,
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
    cls.fields = {"name": 255}
    cls.user = get_user_model().objects.create_user(
        username="testuser",
        email="test@niallbyrne.ca",
        password="test123",
    )
    cls.second_user = get_user_model().objects.create_user(
        username="testuser2",
        email="test2@niallbyrne.ca",
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

    cls.second_store = Store.objects.create(
        user=cls.second_user,
        name="No Frills",
    )
    cls.second_shelf = Shelf.objects.create(
        user=cls.second_user,
        name="Pantry",
    )

    cls.data = {
        'name': "Canned Beans",
        'shelf_life': 99,
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
    self.assertEqual(item.index, self.data['name'].lower())
    self.assertEqual(item.name, self.data['name'])
    self.assertEqual(item.shelf_life, self.data['shelf_life'])
    self.assertEqual(item.user.id, self.user.id)
    self.assertEqual(item.shelf.id, self.shelf.id)
    self.assertEqual(item.price, self.data['price'])
    self.assertEqual(item.quantity, self.data['quantity'])

  def testUnique(self):
    _ = self.sample_item(**self.data)

    with self.assertRaises(ValidationError):
      _ = self.sample_item(**self.data)

    query = Item.objects.filter(name=self.data['name'])
    assert len(query) == 1

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
    self.assertEqual(item.index, sanitized_name.lower())
    self.assertEqual(item.name, sanitized_name)
    self.assertEqual(item.shelf_life, self.data['shelf_life'])
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
    assert item.quantity < MINIMUM_QUANTITY
    with self.assertRaises(ValidationError):
      item.save()

  def testEnormousQuantity(self):
    item = self.sample_item(**self.data)
    item.quantity = 9000000
    assert item.quantity > MAXIMUM_QUANTITY
    with self.assertRaises(ValidationError):
      item.save()

  def testShelfLifeRestrictionsLow(self):
    item = self.sample_item(**self.data)
    item.shelf_life = 0
    assert item.shelf_life < MINIMUM_SHELF_LIFE
    with self.assertRaises(ValidationError):
      item.save()

  def testShelfLifeRestrictionsHigh(self):
    item = self.sample_item(**self.data)
    item.shelf_life = 9000
    assert item.shelf_life > MAXIMUM_SHELF_LIFE
    with self.assertRaises(ValidationError):
      item.save()

  def test_next_expiry_quantity_low(self):
    item = self.sample_item(**self.data)
    item.next_expiry_quantity = -5
    assert item.next_expiry_quantity < MINIMUM_QUANTITY
    with self.assertRaises(ValidationError):
      item.save()

  def test_next_expiry_quantity_high(self):
    item = self.sample_item(**self.data)
    item.next_expiry_quantity = 9000000
    assert item.next_expiry_quantity > MAXIMUM_QUANTITY
    with self.assertRaises(ValidationError):
      item.save()

  def test_expired_low(self):
    item = self.sample_item(**self.data)
    item.expired = -5
    assert item.expired < MINIMUM_QUANTITY
    with self.assertRaises(ValidationError):
      item.save()

  def test_expired_high(self):
    item = self.sample_item(**self.data)
    item.expired = 9000000
    assert item.expired > MAXIMUM_QUANTITY
    with self.assertRaises(ValidationError):
      item.save()

  def test_two_users_with_the_same_item_name(self):
    item1 = self.sample_item(**self.data)

    second_item_definition = dict(self.data)
    second_item_definition['user'] = self.second_user
    second_item_definition['shelf'] = self.second_shelf
    second_item_definition['preferred_stores'] = self.second_store
    item2 = self.sample_item(**second_item_definition)

    self.assertEqual(item1.name, item2.name)
