"""Inventory Transaction Model Managers"""

from datetime import timedelta

from django.db import models
from django.utils.timezone import now


class ExpirationCalculator:
  """Methods to process and move transaction data around.

  :param transaction: A single transaction
  :type transaction: :class:`panic.kitchen.models.transaction.Transaction`
  """

  def __init__(self, transaction):
    self.quantity = transaction.item.quantity
    self.oldest = now()
    self.expired = 0
    self.next_to_expire = 0
    self.instance = transaction

  def update_oldest_expiry(self):
    """If there is no quantity of items marked upcoming to expiry, change the
    oldest date to the current timestamp."""
    if self.next_to_expire < 1:
      self.oldest = now()

  def transaction_date_is_expired(self, transaction):
    """Compares an items transaction date to it's expiration date, to determine
    if the date of the transaction makes the item expired or not.

    :param transaction: A single transaction
    :type transaction: :class:`panic.kitchen.models.transaction.Transaction`
    """
    item_expiry_date = (transaction.datetime.date() +
                        timedelta(days=self.instance.item.shelf_life))
    if now().date() >= item_expiry_date:
      return True
    return False

  def reconcile_transaction_history(self, transaction_history):
    """Iterates through an item's transaction history, updating it's expiry
    information to reconcile the current quantity with the date/time of each
    transaction.

    :param transaction_history: The item's transaction history
    :type transaction_history: :class:`django.db.models.query.QuerySet`s
    """

    for record in transaction_history:
      remaining_inventory_to_check = self.reconcile_single_transaction(record)
      if remaining_inventory_to_check < 1:
        break
      if remaining_inventory_to_check > 0:
        self.quantity = remaining_inventory_to_check
    self.update_oldest_expiry()

  def reconcile_purchase(self, remaining_inventory_to_check, transaction):
    """Handles a positive inventory change, by either debiting the remaining
    count of items that need to be checked, or increasing the count of expired
    items (if those purchased items are already expired).

    :param transaction: A single Transaction
    :type transaction: :class:`panic.kitchen.transaction.Transaction`
    :param remaining_inventory_to_check: The inventory left to check expiry on
    :type remaining_inventory_to_check: int

    :returns: An updated total of remaining_inventory_to_check
    :rtype: int
    """
    self.oldest = transaction.datetime.date()
    remaining_inventory_to_check -= transaction.quantity

    if self.transaction_date_is_expired(transaction):
      self.expired += transaction.quantity
    else:
      self.next_to_expire = min(
          remaining_inventory_to_check + transaction.quantity,
          transaction.quantity)
    return remaining_inventory_to_check

  def reconcile_consumption(self, transaction):
    """Handles a negative inventory change, we assume the oldest items
    are used first, so we debit the calculated expiration total by the number
    of items consumed.

    :param transaction: A single Transaction
    :type transaction: :class:`panic.kitchen.transaction.Transaction`
    """
    self.expired += transaction.quantity

  def reconcile_single_transaction(self, transaction):
    """Processes an individual transaction from a reverse chronology, updating
    the data for expired inventory, and next inventory to expire.

    It returns back the count of inventory that still needs to be processed.

    :param transaction: A single Transaction
    :type transaction: :class:`panic.kitchen.transaction.Transaction`
    """
    remaining_inventory_to_check = self.quantity

    if transaction.quantity > 0:
      remaining_inventory_to_check = self.reconcile_purchase(
          remaining_inventory_to_check, transaction)
    else:
      self.reconcile_consumption(transaction)

    return remaining_inventory_to_check

  def write_expiry_to_model(self):
    """Updates the associated items's expiry information
    from the calculated results."""

    self.instance.item.next_expiry_quantity = self.next_to_expire
    self.instance.item.next_expiry_date = (
        self.oldest + timedelta(days=self.instance.item.shelf_life))
    self.instance.item.expired = max(self.expired, 0)


class ExpiryManager(models.Manager):

  def get_item_history(self, item):
    """Generate a query set representing an item's transaction history.

    :param item: An Item Instance
    :type item: :class:`panic.kitchen.item.Item`
    :returns A queryset containing the results
    :rtype :class:`django.db.models.query.QuerySet`
    """

    return super().get_queryset().filter(item=item).order_by("-datetime")

  def update(self, transaction):
    """Updates the expiry data for an item associated to a transaction.

    :param transaction: A Transaction instance
    :type transaction: :class:`panic.kitchen.transaction.Transaction`
    """

    calculator = ExpirationCalculator(transaction)

    if calculator.quantity > 0:
      item_history = self.get_item_history(calculator.instance.item)
      calculator.reconcile_transaction_history(item_history)

    calculator.write_expiry_to_model()
