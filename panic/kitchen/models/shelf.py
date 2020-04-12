"""User Shelf Model"""

from django.contrib.auth import get_user_model
from django.db import models

from ..fields import BlondeCharField

User = get_user_model()


class Shelf(models.Model):
  """User Shelf Model"""
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  name = BlondeCharField(max_length=255)

  def __str__(self):
    return self.name

  # pylint: disable=W0221
  def save(self, *args, **kwargs):
    self.full_clean()
    return super(Shelf, self).save(*args, **kwargs)
