"""Shared Test Fixtures for Kitchen"""

from ..models.transaction import Transaction


def fixture_create_transaction(user, item, date_object, quantity):
  """Create a test item."""
  transaction = Transaction.objects.create(
      item=item,
      user=user,
      datetime=date_object,
      quantity=quantity,
  )
  return transaction
