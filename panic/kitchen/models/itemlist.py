"""Simple ItemList Model for AutoCompletion"""

from django.db import models

from ..fields import BlondeCharField


class ItemList(models.Model):
  """Items used for AutoCompletion"""
  name = BlondeCharField(max_length=255, unique=True)

  def __str__(self):
    return self.name

  # pylint: disable=W0221
  def save(self, *args, **kwargs):
    self.full_clean()
    return super(ItemList, self).save(*args, **kwargs)
