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

TRANSACTION_QUERY_URL = "kitchen:transaction-detail"


def transaction_query_url(item):
  return reverse(TRANSACTION_QUERY_URL, kwargs={'pk': item})


class PublicTransactionQueryTest(TestCase):
  """Test the public Transaction Query API"""

  def setUp(self) -> None:
    self.client = APIClient()
    self.simulated_item = 1

  def test_list_login_required(self):
    payload = {}
    res = self.client.get(transaction_query_url(self.simulated_item),
                          data=payload)

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
    cls.item1 = Item.objects.create(name="Canned Beans",
                                    shelf_life=99,
                                    user=cls.user,
                                    shelf=cls.shelf,
                                    price=2.00,
                                    quantity=3)
    cls.item1.preferred_stores.add(cls.store)
    cls.item1.save()
    cls.item2 = Item.objects.create(name="Bananas",
                                    shelf_life=99,
                                    user=cls.user,
                                    shelf=cls.shelf,
                                    price=2.00,
                                    quantity=3)
    cls.item2.preferred_stores.add(cls.store)
    cls.item2.save()
    cls.serializer_data = {'item': cls.item1.id, 'quantity': 3}
    cls.object_def1 = {
        'user': cls.user,
        'transaction_date': cls.today,
        'item': cls.item1,
        'quantity': 5
    }
    cls.object_def2 = {
        'user': cls.user,
        'transaction_date': cls.today,
        'item': cls.item1,
        'quantity': 5
    }
    cls.object_def3 = {
        'user': cls.user,
        'transaction_date': cls.today,
        'item': cls.item2,
        'quantity': 5
    }

  def setUp(self):
    self.objects = list()
    self.item1.quantity = 3
    self.item1.save()
    self.client = APIClient()
    self.client.force_authenticate(self.user)

  def tearDown(self) -> None:
    for obj in self.objects:
      obj.delete()

  def test_list_transactions_by_item(self):
    """Test retrieving a list of transactions by item id."""
    self.sample_transaction(**self.object_def1)
    self.sample_transaction(**self.object_def2)
    self.sample_transaction(**self.object_def3)

    res = self.client.get(transaction_query_url(self.item1.id))

    items = Transaction.objects.filter(item=self.item1).order_by("-date")
    serializer = TransactionSerializer(items, many=True)

    assert len(items) == 2
    self.assertEqual(res.status_code, status.HTTP_200_OK)
    self.assertEqual(res.data, serializer.data)

  def test_list_transactions_by_item_opposite_selection(self):
    """Test retrieving a list of transactions by item id."""
    self.sample_transaction(**self.object_def1)
    self.sample_transaction(**self.object_def2)
    self.sample_transaction(**self.object_def3)

    res = self.client.get(transaction_query_url(self.item2.id))

    items = Transaction.objects.filter(item=self.item2).order_by("-date")
    serializer = TransactionSerializer(items, many=True)

    assert len(items) == 1
    self.assertEqual(res.status_code, status.HTTP_200_OK)
    self.assertEqual(res.data, serializer.data)
