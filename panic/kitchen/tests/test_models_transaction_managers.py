"""Test the Transaction Managers and Expiry Calculator."""

from datetime import timedelta
from unittest.mock import Mock, patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from freezegun import freeze_time

import kitchen
from ..models.item import Item
from ..models.shelf import Shelf
from ..models.store import Store
from ..models.transaction import Transaction
from .fixtures import fixture_create_transaction


class TestTransactionManager(TestCase):

  def test_base_test(self):
    raise NotImplementedError("Test Incomplete")


class TestExpiryCalculator(TestCase):

  @classmethod
  @freeze_time("2020-01-14")
  def setUpTestData(cls):
    cls.today = timezone.now()
    cls.tomorrow = timezone.now() + timedelta(days=1)
    cls.yesterday = timezone.now() + timedelta(days=-1)
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
    cls.item = Item.objects.create(
        name="Canned Beans",
        shelf_life=99,
        user=cls.user,
        shelf=cls.shelf,
        price=2.00,
        quantity=3
    )
    cls.item.preferred_stores.add(cls.store)
    cls.item.save()
    cls.transaction1 = {
        'item': cls.item,
        'date_object': cls.today,
        'user': cls.user,
        'quantity': 3
    }
    cls.transaction2 = {
        'item': cls.item,
        'date_object': cls.yesterday,
        'user': cls.user,
        'quantity': 3
    }
    cls.transaction3 = {
        'item': cls.item,
        'date_object': cls.tomorrow,
        'user': cls.user,
        'quantity': 3
    }

  # pylint: disable=R0913
  def sample_transaction(self, user, item, date_object, quantity):
    """Create a test item."""
    transaction = fixture_create_transaction(user, item, date_object, quantity)
    self.objects.append(transaction)
    return transaction

  def create_timebatch(self):
    t_today = self.sample_transaction(**self.transaction1)
    t_yesterday = self.sample_transaction(**self.transaction2)
    t_tomorrow = self.sample_transaction(**self.transaction3)
    return {"today": t_today, "yesterday": t_yesterday, "tomorrow": t_tomorrow}

  def setUp(self):
    self.objects = list()

  def tearDown(self) -> None:
    for obj in self.objects:
      obj.delete()

  def test_get_item_history_is_correct_order(self):
    batch = self.create_timebatch()

    query_set = Transaction.expiration.get_item_history(self.item)

    self.assertEqual(batch['yesterday'].id, query_set[2].id)
    self.assertEqual(batch['today'].id, query_set[1].id)
    self.assertEqual(batch['tomorrow'].id, query_set[0].id)

  def test_get_item_history_is_correct_type(self):
    self.sample_transaction(**self.transaction1)

    query_set = Transaction.expiration.get_item_history(self.item)

    assert len(query_set) == 1
    self.assertIsInstance(query_set[0], Transaction)

  def test_update_with_non_zero_quantity(self):
    transaction = self.sample_transaction(**self.transaction1)

    mock_calculator = Mock()
    mock_reconcile = Mock()
    mock_save = Mock()

    mock_calculator.quantity = 3
    mock_calculator.item = self.item
    mock_calculator.reconcile_transaction_history = mock_reconcile
    mock_calculator.write_expiry_to_item_model = mock_save
    mock_query_set = [1, 2, 3]

    with patch(
        kitchen.__name__ +
        '.models.transaction_managers.ItemExpirationCalculator'
    ) as calculator:
      calculator.return_value = mock_calculator

      with patch(
          kitchen.__name__ +
          '.models.transaction_managers.ExpiryManager.get_item_history'
      ) as mock_get_item_history:
        mock_get_item_history.return_value = mock_query_set

        Transaction.expiration.update(transaction)
        mock_reconcile.assert_called_once_with(mock_query_set)
        mock_save.assert_called_once()

  def test_update_with_zero_quantity(self):
    transaction = self.sample_transaction(**self.transaction1)

    mock_calculator = Mock()
    mock_reconcile = Mock()
    mock_save = Mock()

    mock_calculator.quantity = 0
    mock_calculator.reconcile_transaction_history = mock_reconcile
    mock_calculator.write_expiry_to_item_model = mock_save

    with patch(
        kitchen.__name__ +
        '.models.transaction_managers.ItemExpirationCalculator'
    ) as calculator:
      calculator.return_value = mock_calculator

      Transaction.expiration.update(transaction)

      mock_reconcile.assert_not_called()
      mock_save.assert_called_once()
