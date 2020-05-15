"""Simple ItemList Model for AutoCompletion"""

from django.db import models

from spa_security.fields import BlondeCharField


class ItemList(models.Model):
  """Items used for AutoCompletion"""
  name = BlondeCharField(max_length=255, unique=True)

  def __str__(self):
    return str(self.name)

  # pylint: disable=W0222
  def save(self, *args, **kwargs):
    self.full_clean()
    return super(ItemList, self).save(*args, **kwargs)
