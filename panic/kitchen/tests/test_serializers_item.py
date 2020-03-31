"""Test the Item Serializer."""

from datetime import date

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
    return_list = []
    for key, value in fields.items():
      overloaded = dict()
      overloaded[key] = "abc" * value
      return_list.append(overloaded)
    return return_list

  @classmethod
  def setUpTestData(cls):
    cls.serializer = ItemSerializer
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
    cls.serializer_data = {
        'name': "Canned Beans",
        'bestbefore': cls.today,
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
    self.assertEqual(deserialized['bestbefore'], str(self.today))
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
    self.assertEqual(item.bestbefore, self.today)
    self.assertEqual(item.user.id, self.user.id)
    self.assertEqual(item.shelf.id, self.shelf.id)
    self.assertEqual(item.price, self.serializer_data['price'])
    self.assertEqual(item.quantity, self.serializer_data['quantity'])

    preferred_stores = item.preferred_stores.all()
    assert len(preferred_stores) == 1
    self.assertEqual(preferred_stores[0].id, self.store.id)

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
