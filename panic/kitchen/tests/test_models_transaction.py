"""Test the Item Model."""

from datetime import date as getDate
from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from freezegun import freeze_time

from ..models.item import Item
from ..models.shelf import Shelf
from ..models.store import Store
from ..models.transaction import Transaction


class TestTransaction(TestCase):

  # pylint: disable=R0913
  def sample_transaction(self, user, item, date, quantity):
    """Create a test item."""
    if user is None:
      user = self.user
    transaction = Transaction.objects.create(
        item=item,
        user=user,
        date=date,
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
    cls.today = getDate.today()
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
    cls.positive_data = {
        'item': cls.item,
        'date': cls.today,
        'user': cls.user,
        'quantity': 3
    }
    cls.negative_data = {
        'item': cls.item,
        'date': cls.today,
        'user': cls.user,
        'quantity': -3
    }
    cls.invalid_data = {
        'item': cls.item,
        'date': cls.today,
        'user': cls.user,
        'quantity': -5
    }
    cls.neutral_data = {
        'item': cls.item,
        'date': cls.today,
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
    transaction = query[0]
    self.assertEqual(transaction.item.id, self.item.id)
    self.assertEqual(transaction.date, self.today)
    self.assertEqual(transaction.user.id, self.user.id)
    self.assertEqual(transaction.quantity, self.positive_data['quantity'])
    assert transaction.item.quantity == 6  # The modified value

  def testOperationPositive(self):
    transaction = self.sample_transaction(**self.positive_data)
    self.assertEqual("Purchase", transaction.operation)

  def testStrPositive(self):
    transaction = self.sample_transaction(**self.positive_data)
    string = "Purchase: %s units of %s" % (transaction.quantity,
                                           transaction.item.name)
    self.assertEqual(string, str(transaction))

  def testNegativeTransaction(self):
    self.sample_transaction(**self.negative_data)

    query = Transaction.objects.filter(item=self.item)

    assert len(query) == 1
    transaction = query[0]
    self.assertEqual(transaction.item.id, self.item.id)
    self.assertEqual(transaction.date, self.today)
    self.assertEqual(transaction.user.id, self.user.id)
    self.assertEqual(transaction.quantity, self.negative_data['quantity'])
    assert transaction.item.quantity == 0  # The modified value

  def testOperationNegative(self):
    transaction = self.sample_transaction(**self.negative_data)
    self.assertEqual("Consumption", transaction.operation)

  def testStrNegative(self):
    transaction = self.sample_transaction(**self.negative_data)
    string = "Consumption: %s units of %s" % (transaction.quantity,
                                              transaction.item.name)
    self.assertEqual(string, str(transaction))

  def testInvalidTransaction(self):
    with self.assertRaises(ValidationError):
      self.sample_transaction(**self.invalid_data)

    query = Transaction.objects.filter(item=self.item)
    assert len(query) == 0
    self.item.refresh_from_db()
    assert self.item.quantity == 3  # The original value

  def testNeutralTransaction(self):
    with self.assertRaises(ValidationError):
      self.sample_transaction(**self.neutral_data)

    query = Transaction.objects.filter(item=self.item)
    assert len(query) == 0
    self.item.refresh_from_db()
    assert self.item.quantity == 3  # The original value

  def testOperationNeutral(self):
    transaction = self.sample_transaction(**self.negative_data)
    transaction.quantity = 0
    self.assertIsNone(transaction.operation)
    transaction.quantity = None
    self.assertIsNone(transaction.operation)

  def testStrNeutral(self):
    transaction = self.sample_transaction(**self.negative_data)
    transaction.quantity = 0
    self.assertEqual("Invalid Transaction", str(transaction))


class TestTransactionReconciliation(TestCase):

  # pylint: disable=R0913
  def sample_transaction(self, user, item, date, quantity):
    """Create a test item."""
    if user is None:
      user = self.user
    transaction = Transaction.objects.create(
        item=item,
        user=user,
        date=date,
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

  def setUp(self) -> None:
    self.objects = list()
    self.item.quantity = 3
    self.item.save()

  def tearDown(self) -> None:
    for obj in self.objects:
      obj.delete()

  @freeze_time("2020-01-14")
  def test_next_expiry_date_expired_items(self):
    self.item.quantity = 0
    self.item.save()

    transaction1 = {
        'item': self.item,
        'date': datetime(2000, 1, 1).date(),
        'user': self.user,
        'quantity': 50
    }
    transaction2 = {
        'item': self.item,
        'date': datetime(2010, 2, 1).date(),
        'user': self.user,
        'quantity': -10
    }
    transaction3 = {
        'item': self.item,
        'date': datetime(2011, 1, 1).date(),
        'user': self.user,
        'quantity': 20
    }

    # Transaction 1: sets oldest purchase, but it's already expired
    transaction = self.sample_transaction(**transaction1)
    self.assertEqual(
        transaction.item.next_expiry_date,
        (transaction1['date'] + timedelta(days=transaction.item.shelf_life)))

    # Transaction 2: oldest purchase, but it's already expired
    transaction = self.sample_transaction(**transaction2)
    self.assertEqual(
        transaction.item.next_expiry_date,
        (transaction1['date'] + timedelta(days=transaction.item.shelf_life)))

    # Transaction 3: oldest purchase, but it's already expired
    transaction = self.sample_transaction(**transaction3)
    self.assertEqual(
        transaction.item.next_expiry_date,
        (transaction1['date'] + timedelta(days=transaction.item.shelf_life)))

    # All Items Are Expired
    self.assertEqual(
        transaction.item.expired, transaction1['quantity'] +
        transaction2['quantity'] + transaction3['quantity'])

    # No upcoming expirations
    self.assertEqual(transaction.item.next_expiry_quantity, 0)

  @freeze_time("2020-01-14")
  def test_next_expiry_date_some_expired_items(self):
    self.item.quantity = 0
    self.item.save()

    transaction1 = {
        'item': self.item,
        'date': datetime(2000, 1, 1).date(),
        'user': self.user,
        'quantity': 50
    }
    transaction2 = {
        'item': self.item,
        'date': datetime.now().date(),
        'user': self.user,
        'quantity': 10
    }

    # Transaction 1: sets oldest purchase
    transaction = self.sample_transaction(**transaction1)
    self.assertEqual(
        transaction.item.next_expiry_date,
        (transaction1['date'] + timedelta(days=transaction.item.shelf_life)))

    # Transaction 2: oldest purchase should remain the same
    transaction = self.sample_transaction(**transaction2)
    self.assertEqual(
        transaction.item.next_expiry_date,
        (transaction1['date'] + timedelta(days=transaction.item.shelf_life)))

    # Some Items Are Expired
    self.assertEqual(transaction.item.expired, transaction1['quantity'])

    # An upcoming expiry
    self.assertEqual(transaction.item.next_expiry_quantity,
                     transaction2['quantity'])

  @freeze_time("2020-01-14")
  def test_next_expiry_date_no_expired_items(self):

    self.item.quantity = 0
    self.item.save()

    transaction1 = {
        'item': self.item,
        'date': datetime.now().date(),
        'user': self.user,
        'quantity': 50
    }
    transaction2 = {
        'item': self.item,
        'date': datetime.now().date(),
        'user': self.user,
        'quantity': -10
    }

    # Transaction 1: sets oldest purchase
    transaction = self.sample_transaction(**transaction1)
    self.assertEqual(
        transaction.item.next_expiry_date,
        (transaction1['date'] + timedelta(days=transaction.item.shelf_life)))

    # Transaction 2: oldest purchase should remain the same
    transaction = self.sample_transaction(**transaction2)
    self.assertEqual(
        transaction.item.next_expiry_date,
        (transaction2['date'] + timedelta(days=transaction.item.shelf_life)))

    # No Items Are Expired
    self.assertEqual(transaction.item.expired, 0)

    # An upcoming expiry
    self.assertEqual(transaction.item.next_expiry_quantity,
                     transaction1['quantity'] + transaction2['quantity'])

  @freeze_time("2020-01-14")
  def test_next_expiry_date_no_items(self):
    transaction1 = {
        'item': self.item,
        'date': datetime(2000, 1, 1).date(),
        'user': self.user,
        'quantity': 50
    }
    transaction2 = {
        'item': self.item,
        'date': datetime.now().date(),
        'user': self.user,
        'quantity': -50
    }

    # Transaction 1: sets oldest purchase
    transaction = self.sample_transaction(**transaction1)
    self.assertEqual(
        transaction.item.next_expiry_date,
        (transaction1['date'] + timedelta(days=transaction.item.shelf_life)))

    # Transaction 2: oldest purchase should remain the same
    transaction = self.sample_transaction(**transaction2)
    self.assertEqual(
        transaction.item.next_expiry_date,
        (transaction1['date'] + timedelta(days=transaction.item.shelf_life)))

    # No Items Are Expired
    self.assertEqual(transaction.item.expired, 0)

    # No upcoming expiry
    self.assertEqual(transaction.item.next_expiry_quantity, 0)

  @freeze_time("2020-01-14")
  def test_expiry_some_expired_some_consumed_items(self):
    self.item.quantity = 0
    self.item.save()

    transaction1 = {
        'item': self.item,
        'date': datetime(2000, 1, 1).date(),
        'user': self.user,
        'quantity': 50
    }
    transaction2 = {
        'item': self.item,
        'date': datetime(2010, 1, 1).date(),
        'user': self.user,
        'quantity': -10
    }
    transaction3 = {
        'item': self.item,
        'date': datetime(2011, 1, 1).date(),
        'user': self.user,
        'quantity': -10
    }
    transaction4 = {
        'item': self.item,
        'date': datetime.now().date(),
        'user': self.user,
        'quantity': 10
    }

    # Transaction 1: sets oldest purchase
    transaction = self.sample_transaction(**transaction1)
    self.assertEqual(
        transaction.item.next_expiry_date,
        (transaction1['date'] + timedelta(days=transaction.item.shelf_life)))

    # Transaction 2: oldest purchase should remain the same
    transaction = self.sample_transaction(**transaction2)
    self.assertEqual(
        transaction.item.next_expiry_date,
        (transaction1['date'] + timedelta(days=transaction.item.shelf_life)))

    # Transaction 3: oldest purchase should remain the same
    transaction = self.sample_transaction(**transaction3)
    self.assertEqual(
        transaction.item.next_expiry_date,
        (transaction1['date'] + timedelta(days=transaction.item.shelf_life)))

    # Transaction 4: oldest purchase should remain the same
    transaction = self.sample_transaction(**transaction4)
    self.assertEqual(
        transaction.item.next_expiry_date,
        (transaction1['date'] + timedelta(days=transaction.item.shelf_life)))

    # Some Items Are Expired
    self.assertEqual(transaction.item.expired, 30)

    # An upcoming expiry
    self.assertEqual(transaction.item.next_expiry_quantity, 10)
