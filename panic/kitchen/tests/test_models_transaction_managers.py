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
from ..models.transaction_managers import ItemExpirationCalculator
from .fixtures import fixture_create_transaction


class MockExpiryCalculator:
  mock = Mock()
  mock_reconcile = Mock()
  mock_save = Mock()
  quantity = None
  item = None
  reconcile_transaction_history = None
  write_expiry_to_item_model = None

  @classmethod
  def reset(cls):
    cls.mock.reset_mock()
    cls.mock_reconcile.reset_mock()
    cls.mock_save.reset_mock()

  @classmethod
  def configure(cls, item, quantity):
    cls.reset()

    cls.quantity = quantity
    cls.item = item
    cls.reconcile_transaction_history = cls.mock_reconcile
    cls.write_expiry_to_item_model = cls.mock_save


class TestHarnessWithTestData(TestCase):

  @classmethod
  @freeze_time("2020-01-14")
  def setUpTestData(cls):
    cls.today = timezone.now()
    cls.tomorrow = timezone.now() + timedelta(days=1)
    cls.yesterday = timezone.now() + timedelta(days=-1)
    cls.last_year = timezone.now() + timedelta(days=-365)
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
    cls.transaction4 = {
        'item': cls.item,
        'date_object': cls.last_year,
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
    self.item.expired = 0
    self.item.quantity = 3
    self.item.next_to_expire = 0
    self.item.save()


class TestItemExpirationCalculator(TestHarnessWithTestData):

  def create_batch_with_total(self):
    batch = self.create_timebatch()

    total_quantity = 0
    total_quantity += batch['yesterday'].quantity
    total_quantity += batch['today'].quantity
    total_quantity += batch['tomorrow'].quantity
    return batch, total_quantity

  @freeze_time("2020-01-14")
  def test_reconcile_transaction_history(self):
    self.create_timebatch()

    with patch(
        kitchen.__name__ +
        '.models.transaction_managers.ItemExpirationCalculator'
        '.reconcile_single_transaction'
    ) as reconciler:

      reconciler.side_effect = [3, 2, 0]
      calculator = ItemExpirationCalculator(self.item)
      calculator.oldest = self.last_year
      history = [1, 2, 3]
      calculator.reconcile_transaction_history(history)

      reconciler.assert_any_call(history[0])
      reconciler.assert_any_call(history[1])
      reconciler.assert_any_call(history[2])
      assert reconciler.call_count == 3
      assert calculator.quantity == 2
      assert calculator.oldest == timezone.now()

  @freeze_time("2020-01-14")
  def test_reconcile_transaction_history_with_expired(self):
    self.create_timebatch()

    with patch(
        kitchen.__name__ +
        '.models.transaction_managers.ItemExpirationCalculator'
        '.reconcile_single_transaction'
    ) as reconciler:
      reconciler.side_effect = [3, 2, 0]
      calculator = ItemExpirationCalculator(self.item)
      calculator.next_to_expire = 1
      calculator.oldest = self.last_year
      history = [1, 2, 3]
      calculator.reconcile_transaction_history(history)

      reconciler.assert_any_call(history[0])
      reconciler.assert_any_call(history[1])
      reconciler.assert_any_call(history[2])
      assert reconciler.call_count == 3
      assert calculator.quantity == 2
      assert calculator.oldest == self.last_year

  def test_write_expiry_to_item_model_expired_items(self):
    next_to_expire = 1
    oldest = self.last_year
    expired = 5

    calculator = ItemExpirationCalculator(self.item)
    calculator.next_to_expire = next_to_expire
    calculator.oldest = oldest
    calculator.expired = expired

    calculator.write_expiry_to_item_model()

    assert self.item.next_expiry_quantity == next_to_expire
    assert self.item.next_expiry_date == (
        self.last_year + timedelta(days=self.item.shelf_life)
    )
    assert self.item.expired == expired

  def test_write_expiry_to_item_model_neg_expired_items(self):
    next_to_expire = 1
    oldest = self.last_year
    expired = -5

    calculator = ItemExpirationCalculator(self.item)
    calculator.next_to_expire = next_to_expire
    calculator.oldest = oldest
    calculator.expired = expired

    calculator.write_expiry_to_item_model()

    assert self.item.next_expiry_quantity == next_to_expire
    assert self.item.next_expiry_date == (
        self.last_year + timedelta(days=self.item.shelf_life)
    )
    assert self.item.expired == 0

  @freeze_time("2020-01-14")
  def test_reconcile_single_transaction_pos_qty(self):
    batch, total_quantity = self.create_batch_with_total()

    calculator = ItemExpirationCalculator(self.item)
    result = calculator.reconcile_single_transaction(batch['yesterday'])
    self.assertEqual(result, total_quantity)
    self.assertEqual(calculator.expired, 0)

  @freeze_time("2021-01-14")
  def test_reconcile_single_transaction_pos_qty_future(self):
    batch, total_quantity = self.create_batch_with_total()

    calculator = ItemExpirationCalculator(self.item)
    result = calculator.reconcile_single_transaction(batch['yesterday'])
    self.assertEqual(result, total_quantity)
    self.assertEqual(calculator.expired, batch['yesterday'].quantity)

  @freeze_time("2020-01-14")
  def test_reconcile_single_transaction_neg_qty(self):
    batch, total_quantity = self.create_batch_with_total()

    batch['yesterday'].quantity = -3
    batch['yesterday'].save()

    calculator = ItemExpirationCalculator(self.item)
    result = calculator.reconcile_single_transaction(batch['yesterday'])
    self.assertEqual(result, total_quantity)
    self.assertEqual(calculator.expired, -3)

  @freeze_time("2021-01-14")
  def test_reconcile_single_transaction_neg_qty_future(self):
    batch, total_quantity = self.create_batch_with_total()

    batch['yesterday'].quantity = -3
    batch['yesterday'].save()

    calculator = ItemExpirationCalculator(self.item)
    result = calculator.reconcile_single_transaction(batch['yesterday'])
    self.assertEqual(result, total_quantity)
    self.assertEqual(calculator.expired, -3)


class TestExpiryManager(TestHarnessWithTestData):

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
    MockExpiryCalculator.configure(self.item, 3)
    mock_query_set = [1, 2, 3]

    with patch(
        kitchen.__name__ +
        '.models.transaction_managers.ItemExpirationCalculator'
    ) as calculator:
      calculator.return_value = MockExpiryCalculator

      with patch(
          kitchen.__name__ +
          '.models.transaction_managers.ExpiryManager.get_item_history'
      ) as mock_get_item_history:

        mock_get_item_history.return_value = mock_query_set
        Transaction.expiration.update(transaction)
        MockExpiryCalculator.mock_reconcile.assert_called_once_with(
            mock_query_set
        )
        MockExpiryCalculator.mock_save.assert_called_once()

  def test_update_with_zero_quantity(self):
    transaction = self.sample_transaction(**self.transaction1)

    MockExpiryCalculator.configure(self.item, 0)

    with patch(
        kitchen.__name__ +
        '.models.transaction_managers.ItemExpirationCalculator'
    ) as calculator:

      calculator.return_value = MockExpiryCalculator
      Transaction.expiration.update(transaction)
      MockExpiryCalculator.mock_reconcile.assert_not_called()
      MockExpiryCalculator.mock_save.assert_called_once()
