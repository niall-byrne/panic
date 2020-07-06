"""Test the Transaction Serializer."""

import datetime

import pytz
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from freezegun import freeze_time
from rest_framework.serializers import ValidationError

from ..models.item import Item
from ..models.shelf import Shelf
from ..models.store import Store
from ..models.transaction import Transaction
from ..serializers.transaction import TransactionSerializer


class MockRequest:

  def __init__(self, user):
    self.user = user


def deserialize_datetime(string):
  return pytz.utc.localize(
      datetime.datetime.strptime(string, "%Y-%m-%dT%H:%M:%SZ"))


class TestItem(TestCase):

  # pylint: disable=R0913
  def sample_transaction(self, user, item, transaction_date, quantity):
    """Create a test item."""
    if user is None:
      user = self.user
    transaction = Transaction.objects.create(
        item=item,
        user=user,
        datetime=transaction_date,
        quantity=quantity,
    )
    self.objects.append(transaction)
    return transaction

  @staticmethod
  def generate_overload(fields):
    return_list = []
    for key, value in fields.items():
      overloaded = dict()
      overloaded[key] = "abc" * value
      return_list.append(overloaded)
    return return_list

  @classmethod
  @freeze_time('2020-01-14')
  def setUpTestData(cls):
    cls.serializer = TransactionSerializer
    cls.today = timezone.now()
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
    cls.item = Item.objects.create(name="Canned Beans",
                                   shelf_life=99,
                                   user=cls.user,
                                   shelf=cls.shelf,
                                   price=2.00,
                                   quantity=3)
    cls.item.preferred_stores.add(cls.store)
    cls.item.save()
    cls.data = {
        'item': cls.item,
        'transaction_date': cls.today,
        'user': cls.user,
        'quantity': 3
    }
    cls.serializer_data = {
        'item': cls.item.id,
        'datetime': cls.today,
        'quantity': 3
    }
    cls.request = MockRequest(cls.user)

  def setUp(self):
    self.objects = list()
    self.item.quantity = 3
    self.item.save()

  def tearDown(self) -> None:
    for obj in self.objects:
      obj.delete()

  def testDeserialize(self):
    transaction = self.sample_transaction(**self.data)
    serialized = self.serializer(transaction)
    deserialized = serialized.data

    self.assertEqual(deserialize_datetime(deserialized['datetime']), self.today)
    self.assertEqual(deserialized['item'], self.item.id)
    self.assertEqual(deserialized['quantity'], self.data['quantity'])
    assert 'user' not in deserialized

  def testSerialize(self):
    serialized = self.serializer(
        context={'request': self.request},
        data=self.serializer_data,
    )
    serialized.is_valid(raise_exception=True)
    serialized.save()

    query = Transaction.objects.filter(user=self.user.id)

    assert len(query) == 1
    transaction = query[0]

    self.assertEqual(transaction.user.id, self.user.id)
    self.assertEqual(transaction.item.id, self.item.id)
    self.assertEqual(transaction.datetime, self.today)
    self.assertEqual(transaction.quantity, self.serializer_data['quantity'])

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
