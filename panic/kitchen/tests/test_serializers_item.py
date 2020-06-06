"""Test the Item Serializer."""

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.serializers import ValidationError

from ..models.item import Item
from ..models.shelf import Shelf
from ..models.store import Store
from ..serializers.item import ItemSerializer


class MockRequest:

  def __init__(self, user):
    self.user = user


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
    return_list = []
    for key, value in fields.items():
      overloaded = dict()
      overloaded[key] = "abc" * value
      return_list.append(overloaded)
    return return_list

  @classmethod
  def setUpTestData(cls):
    cls.serializer = ItemSerializer
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
        'shelf_life': 99,
        'user': cls.user,
        'shelf': cls.shelf,
        'preferred_stores': cls.store,
        'price': 2.00,
        'quantity': 3
    }
    cls.serializer_data = {
        'name': "Canned Beans",
        'shelf_life': 109,
        'shelf': cls.shelf.id,
        'preferred_stores': [cls.store.id],
        'price': 2.00,
        'quantity': 3
    }
    cls.request = MockRequest(cls.user)

  def setUp(self):
    self.objects = list()

  def tearDown(self) -> None:
    for obj in self.objects:
      obj.delete()

  def testDeserialize(self):
    item = self.sample_item(**self.data)
    serialized = self.serializer(item)
    deserialized = serialized.data

    price = '2.00'

    self.assertEqual(deserialized['name'], self.data['name'])
    self.assertEqual(deserialized['shelf_life'], self.data['shelf_life'])
    self.assertEqual(deserialized['shelf'], self.shelf.id)
    self.assertEqual(deserialized['price'], price)
    self.assertEqual(deserialized['quantity'], self.data['quantity'])
    preferred_stores = [store.id for store in item.preferred_stores.all()]
    self.assertEqual(deserialized['preferred_stores'], preferred_stores)
    assert 'user' not in deserialized

  def testSerialize(self):
    serialized = self.serializer(
        context={'request': self.request},
        data=self.serializer_data,
    )
    serialized.is_valid(raise_exception=True)
    serialized.save()

    query = Item.objects.filter(name=self.serializer_data['name'])

    assert len(query) == 1
    item = query[0]

    self.assertEqual(item.name, self.serializer_data['name'])
    self.assertEqual(item.shelf_life, self.serializer_data['shelf_life'])
    self.assertEqual(item.user.id, self.user.id)
    self.assertEqual(item.shelf.id, self.shelf.id)
    self.assertEqual(item.price, self.serializer_data['price'])
    self.assertEqual(item.quantity, self.serializer_data['quantity'])

  def testUniqueConstraint(self):
    serialized = self.serializer(
        context={'request': self.request},
        data=self.serializer_data,
    )
    serialized.is_valid(raise_exception=True)
    serialized.save()

    serialized2 = self.serializer(
        context={'request': self.request},
        data=self.serializer_data,
    )
    with self.assertRaises(ValidationError):
      serialized2.is_valid(raise_exception=True)

  def testFieldLengths(self):
    overloads = self.generate_overload(self.fields)
    for overload in overloads:
      local_data = dict(self.data)
      local_data.update(overload)
      with self.assertRaises(ValidationError):
        serialized = self.serializer(
            context={'request': self.request},
            data=local_data,
        )
        serialized.is_valid(raise_exception=True)
