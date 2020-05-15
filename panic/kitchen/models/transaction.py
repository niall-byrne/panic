"""Inventory Transaction Model"""

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models, transaction

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
  date = models.DateField()
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
      self.item.quantity = self.item.quantity + self.quantity
      self.item.save()
      return super(Transaction, self).save(*args, **kwargs)
