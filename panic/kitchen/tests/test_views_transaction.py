"""Test the Transaction API."""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.utils.http import urlencode
from freezegun import freeze_time
from rest_framework import status
from rest_framework.test import APIClient

from ..models.item import Item
from ..models.shelf import Shelf
from ..models.store import Store
from ..models.transaction import Transaction
from ..serializers.transaction import TransactionSerializer

TRANSACTION_URL = reverse("kitchen:transactions-list")


def transaction_query_url(query_kwargs={}):  # pylint: disable=W0102
  return '{}?{}'.format(TRANSACTION_URL, urlencode(query_kwargs))


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
        datetime=transaction_date,
        quantity=quantity,
    )
    self.objects.append(transaction)
    return transaction

  @classmethod
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
    cls.item1 = Item.objects.create(
        name="Canned Beans",
        shelf_life=99,
        user=cls.user,
        shelf=cls.shelf,
        price=2.00,
        quantity=3
    )
    cls.item1.preferred_stores.add(cls.store)
    cls.item1.save()
    cls.item2 = Item.objects.create(
        name="Bananas",
        shelf_life=99,
        user=cls.user,
        shelf=cls.shelf,
        price=2.00,
        quantity=3
    )
    cls.item2.preferred_stores.add(cls.store)
    cls.item2.save()
    cls.serializer_data = {'item': cls.item1.id, 'quantity': 3}
    cls.object_def1 = {
        'user': cls.user,
        'transaction_date': timezone.now(),
        'item': cls.item1,
        'quantity': 5
    }
    cls.object_def2 = {
        'user': cls.user,
        'transaction_date': timezone.now(),
        'item': cls.item1,
        'quantity': 5
    }
    cls.object_def3 = {
        'user': cls.user,
        'transaction_date': timezone.now(),
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

  @freeze_time("2014-01-01")
  def test_create_transaction(self):
    """Test creating a transaction."""
    res = self.client.post(TRANSACTION_URL, data=self.serializer_data)

    items = Transaction.objects.all()
    self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    assert len(items) == 1
    transaction = items[0]

    self.assertEqual(transaction.user.id, self.user.id)
    self.assertEqual(transaction.item.id, self.item1.id)
    self.assertEqual(transaction.datetime, timezone.now())
    self.assertEqual(transaction.quantity, self.serializer_data['quantity'])
    assert transaction.item.quantity == 6  # The modified value

  def test_list_all_transactions(self):
    """Test retrieving a list of all user transactions."""
    self.sample_transaction(**self.object_def1)
    self.sample_transaction(**self.object_def2)
    self.sample_transaction(**self.object_def3)

    res = self.client.get(transaction_query_url())

    items = Transaction.objects.all().order_by("-datetime")
    serializer = TransactionSerializer(items, many=True)

    assert len(items) == 3
    self.assertEqual(res.status_code, status.HTTP_200_OK)
    print(res.data['results'])
    self.assertEqual(res.data['results'], serializer.data)

  def test_list_transactions_by_item_filter(self):
    """Test retrieving a list of transactions by item id."""
    self.sample_transaction(**self.object_def1)
    self.sample_transaction(**self.object_def2)
    self.sample_transaction(**self.object_def3)

    res = self.client.get(transaction_query_url({"item": self.item1.id}))

    items = Transaction.objects.filter(item=self.item1).order_by("-datetime")
    serializer = TransactionSerializer(items, many=True)

    assert len(items) == 2
    self.assertEqual(res.status_code, status.HTTP_200_OK)
    self.assertEqual(res.data['results'], serializer.data)

  def test_list_transactions_by_another_item_filter(self):
    """Test retrieving a list of transactions by item id."""
    self.sample_transaction(**self.object_def1)
    self.sample_transaction(**self.object_def2)
    self.sample_transaction(**self.object_def3)

    res = self.client.get(transaction_query_url({"item": self.item2.id}))

    items = Transaction.objects.filter(item=self.item2).order_by("-datetime")
    serializer = TransactionSerializer(items, many=True)

    assert len(items) == 1
    self.assertEqual(res.status_code, status.HTTP_200_OK)
    self.assertEqual(res.data['results'], serializer.data)

  def test_list_transactions_paginated_correctly(self):
    """Test that retrieving a list of transactions is limited correctly."""
    for _ in range(0, 11):
      self.sample_transaction(**self.object_def1)

    res = self.client.get(
        transaction_query_url({
            "item": self.item1.id,
            "page_size": 10
        })
    )
    self.assertEqual(len(res.data['results']), 10)
    self.assertIsNotNone(res.data['next'])
    self.assertIsNone(res.data['previous'])
