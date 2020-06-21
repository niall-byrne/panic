"""Test the Transaction API."""

from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from ..models.item import Item
from ..models.shelf import Shelf
from ..models.store import Store
from ..models.transaction import Transaction
from ..serializers.transaction import TransactionSerializer

TRANSACTION_URL = reverse("kitchen:transaction-list")


class PublicItemTest(TestCase):
  """Test the public Transaction API"""

  def setUp(self) -> None:
    self.client = APIClient()

  def test_create_login_required(self):
    payload = {}
    res = self.client.post(TRANSACTION_URL, data=payload)

    self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateItemTest(TestCase):
  """Test the authorized Transaction API"""

  # pylint: disable=R0913
  def sample_transaction(self, user, item, transaction_date, quantity):
    """Create a test item."""
    if user is None:
      user = self.user
    transaction = Transaction.objects.create(
        item=item,
        user=user,
        date=transaction_date,
        quantity=quantity,
    )
    self.objects.append(transaction)
    return transaction

  @classmethod
  def setUpTestData(cls):
    cls.serializer = TransactionSerializer
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
                                   shelf_life=99,
                                   user=cls.user,
                                   shelf=cls.shelf,
                                   price=2.00,
                                   quantity=3)
    cls.item.preferred_stores.add(cls.store)
    cls.item.save()
    cls.serializer_data = {'item': cls.item.id, 'quantity': 3}

  def setUp(self):
    self.objects = list()
    self.item.quantity = 3
    self.item.save()
    self.client = APIClient()
    self.client.force_authenticate(self.user)

  def tearDown(self) -> None:
    for obj in self.objects:
      obj.delete()

  def test_create_transaction(self):
    """Test creating a transaction."""
    res = self.client.post(TRANSACTION_URL, data=self.serializer_data)

    items = Transaction.objects.all()
    self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    assert len(items) == 1
    transaction = items[0]

    self.assertEqual(transaction.user.id, self.user.id)
    self.assertEqual(transaction.item.id, self.item.id)
    self.assertEqual(transaction.date, self.today)
    self.assertEqual(transaction.quantity, self.serializer_data['quantity'])
    assert transaction.item.quantity == 6  # The modified value
