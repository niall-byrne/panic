"""Classes dedicated to data processing."""

from datetime import timedelta

from django.utils.timezone import now


class TransactionProcessor:
  """Methods to process and move transaction data around."""

  def __init__(self, instance):
    self.quantity = instance.item.quantity
    self.oldest = now()
    self.expired = 0
    self.next_to_expire = 0
    self.instance = instance

  def is_expired(self, selection):
    if now().date() >= (selection.date +
                        timedelta(days=self.instance.item.shelf_life)):
      return True
    return False

  def reconcile_transaction(self, record):
    """Processes an individual transaction from a reverse chronology, updating
    the data for expired inventory, and next inventory to expire.

    It returns back the count of inventory that still needs to be processed.
    """
    remaining = self.quantity
    if record.quantity > 0:
      self.oldest = record.date
      remaining -= record.quantity
      if self.is_expired(record):
        self.expired = self.expired + record.quantity
      else:
        self.next_to_expire = min(remaining + record.quantity, record.quantity)
    else:
      self.expired += record.quantity
    return remaining
