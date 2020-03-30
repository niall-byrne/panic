"""Test the Item Model."""

from datetime import date

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from ..models.item import Item
from ..models.shelf import Shelf
from ..models.store import Store
from ..models.transaction import Transaction


class TestItem(TestCase):

  # pylint: disable=R0913
  def sample_transaction(self, user, item, purchase_date, quantity):
    """Create a test item."""
    if user is None:
      user = self.user
    transaction = Transaction.objects.create(
        item=item,
        user=user,
        date=purchase_date,
        quantity=quantity,
    )
    self.objects.append(transaction)
    return transaction

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
    cls.item = Item.objects.create(name="Canned Beans",
                                   bestbefore=cls.today,
                                   user=cls.user,
                                   shelf=cls.shelf,
                                   price=2.00,
                                   quantity=3)
    cls.item.preferred_stores.add(cls.store)
    cls.item.save()
    cls.positive_data = {
        'item': cls.item,
        'purchase_date': cls.today,
        'user': cls.user,
        'quantity': 3
    }
    cls.negative_data = {
        'item': cls.item,
        'purchase_date': cls.today,
        'user': cls.user,
        'quantity': -3
    }
    cls.invalid_data = {
        'item': cls.item,
        'purchase_date': cls.today,
        'user': cls.user,
        'quantity': -5
    }
    cls.neutral_data = {
        'item': cls.item,
        'purchase_date': cls.today,
        'user': cls.user,
        'quantity': 0
    }

  def setUp(self) -> None:
    self.objects = list()
    self.item.quantity = 3
    self.item.save()

  def tearDown(self) -> None:
    for obj in self.objects:
      obj.delete()

  def testPositiveTransaction(self):
    self.sample_transaction(**self.positive_data)

    query = Transaction.objects.filter(item=self.item)

    assert len(query) == 1
    purchase = query[0]
    self.assertEqual(purchase.item.id, self.item.id)
    self.assertEqual(purchase.date, self.today)
    self.assertEqual(purchase.user.id, self.user.id)
    self.assertEqual(purchase.quantity, self.positive_data['quantity'])

  def testOperationPositive(self):
    purchase = self.sample_transaction(**self.positive_data)
    self.assertEqual("Purchase", purchase.operation)

  def testStrPositive(self):
    purchase = self.sample_transaction(**self.positive_data)
    string = "Purchase: %s units of %s" % (purchase.quantity,
                                           purchase.item.name)
    self.assertEqual(string, str(purchase))

  def testNegativeTransaction(self):
    self.sample_transaction(**self.negative_data)

    query = Transaction.objects.filter(item=self.item)

    assert len(query) == 1
    purchase = query[0]
    self.assertEqual(purchase.item.id, self.item.id)
    self.assertEqual(purchase.date, self.today)
    self.assertEqual(purchase.user.id, self.user.id)
    self.assertEqual(purchase.quantity, self.negative_data['quantity'])

  def testOperationNegative(self):
    purchase = self.sample_transaction(**self.negative_data)
    self.assertEqual("Consumption", purchase.operation)

  def testStrNegative(self):
    purchase = self.sample_transaction(**self.negative_data)
    string = "Consumption: %s units of %s" % (purchase.quantity,
                                              purchase.item.name)
    self.assertEqual(string, str(purchase))

  def testInvalidTransaction(self):
    with self.assertRaises(ValidationError):
      self.sample_transaction(**self.invalid_data)

    query = Transaction.objects.filter(item=self.item)
    assert len(query) == 0
    assert self.item.quantity == 3  # The original value

  def testNeutralTransaction(self):
    with self.assertRaises(ValidationError):
      self.sample_transaction(**self.neutral_data)

    query = Transaction.objects.filter(item=self.item)
    assert len(query) == 0
    assert self.item.quantity == 3  # The original value

  def testOperationNeutral(self):
    purchase = self.sample_transaction(**self.negative_data)
    purchase.quantity = 0
    self.assertIsNone(purchase.operation)
    purchase.quantity = None
    self.assertIsNone(purchase.operation)

  def testStrNeutral(self):
    purchase = self.sample_transaction(**self.negative_data)
    purchase.quantity = 0
    self.assertEqual("Invalid Transaction", str(purchase))
