"""Simple ItemList Model for AutoCompletion"""

from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

from .shelf import Shelf
from .store import Store

User = get_user_model()

TWOPLACES = Decimal(10)**-2


class Item(models.Model):
  """Items used for AutoCompletion"""
  name = models.CharField(max_length=255)
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

  def __str__(self):
    return self.name
