"""Inventory Transaction Model"""

from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.utils.timezone import now

from ..processors import TransactionProcessor
from .item import Item

User = get_user_model()


def validate_quantity(value):
  if value == 0:
    raise ValidationError([{'quantity': "Must not be equal to 0"}])
  return value


class Transaction(models.Model):
  """Inventory Transaction Model"""
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  item = models.ForeignKey(Item, on_delete=models.CASCADE)
  datetime = models.DateTimeField(default=now)
  quantity = models.IntegerField(validators=[validate_quantity])

  class Meta:
    indexes = [
        models.Index(fields=['datetime']),
    ]

  @property
  def operation(self):
    if isinstance(self.quantity, int):
      if self.quantity > 0:
        return "Purchase"
      if self.quantity < 0:
        return "Consumption"
    return None

  def __str__(self):
    operation_type = self.operation
    if operation_type:
      return "%s: %s units of %s" % (
          self.operation,
          self.quantity,
          self.item.name,
      )
    return "Invalid Transaction"

  def update_related_item_expiry(self):
    """Calculates the expiry of the oldest purchase in your inventory of a
    specific item.  Creates a count of expired items, and marks a quantity of
    items as "next to expire".
    """
    processor = TransactionProcessor(self)

    if processor.quantity > 0:
      query_set = self.__class__.objects.filter(
          item=self.item).order_by("-datetime")
      for record in query_set:
        remaining = processor.reconcile_transaction(record)
        if remaining < 1:
          break
        processor.quantity = remaining
      if processor.next_to_expire < 1:
        processor.oldest = now()

    self.item.next_expiry_quantity = processor.next_to_expire
    self.item.next_expiry_date = (processor.oldest +
                                  timedelta(days=self.item.shelf_life))
    self.item.expired = max(processor.expired, 0)

  def update_related_item_quantity(self):
    self.item.quantity = self.item.quantity + self.quantity

  def clean(self):
    if (self.item.quantity + self.quantity) < 0:
      raise ValidationError([{
          'quantity': "This field may not reduce inventory below 0."
      }])
    super().clean()

  # pylint: disable=W0222
  def save(self, *args, **kwargs):
    with transaction.atomic():
      self.full_clean()
      super(Transaction, self).save(*args, **kwargs)
      self.update_related_item_quantity()
      self.update_related_item_expiry()
      self.item.save()
