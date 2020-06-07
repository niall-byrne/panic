"""Inventory Transaction Model"""

from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.utils.timezone import now

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
  date = models.DateField(default=now)
  quantity = models.IntegerField(validators=[validate_quantity])

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

  def is_expired(self, selection):
    if now().date() >= (selection.date + timedelta(days=self.item.shelf_life)):
      return True
    return False

  def update_related_item_expiry(self):
    """Calculates the expiry of the oldest purchase in your inventory of a
    specific item.  Creates a count of expired items, and marks a quantity of
    items as "next to expire".
    """
    quantity = self.item.quantity
    oldest = self.date
    expired = 0
    next_to_expire = 0

    if quantity > 1:
      query_set = self.__class__.objects.filter(
          item=self.item).order_by("-date")
      for record in query_set:
        remaining = quantity
        if record.quantity > 0:
          oldest = record.date
          remaining = quantity - record.quantity
          if self.is_expired(record):
            expired = expired + record.quantity
          else:
            next_to_expire = min(remaining + record.quantity, record.quantity)
        else:
          expired = expired + record.quantity
        if remaining < 1:
          break
        quantity = remaining

    self.item.next_expiry_date = (oldest + timedelta(days=self.item.shelf_life))
    self.item.expired = expired
    self.item.next_expiry_quantity = next_to_expire

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
