"""Simple ItemList Model for AutoCompletion"""

from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

from spa_security.fields import BlondeCharField
from .shelf import Shelf
from .store import Store

User = get_user_model()

TWOPLACES = Decimal(10)**-2


class Item(models.Model):
  """Items used for AutoCompletion"""
  name = BlondeCharField(max_length=255, unique=True)
  bestbefore = models.DateField()
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  shelf = models.ForeignKey(Shelf, on_delete=models.CASCADE)
  preferred_stores = models.ManyToManyField(Store)
  price = models.DecimalField(max_digits=10, decimal_places=2)
  quantity = models.IntegerField(
      default=0,
      validators=[
          MinValueValidator(0),
      ],
  )

  class Meta:
    constraints = [
        models.UniqueConstraint(fields=['user', 'name'], name='item per user')
    ]

  def __str__(self):
    return str(self.name)

  # pylint: disable=W0222
  def save(self, *args, **kwargs):
    self.full_clean()
    return super(Item, self).save(*args, **kwargs)
