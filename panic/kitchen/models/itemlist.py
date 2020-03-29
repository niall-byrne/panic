"""Simple ItemList Model for AutoCompletion"""

from django.db import models


class ItemList(models.Model):
  """Items used for AutoCompletion"""
  name = models.CharField(max_length=255)

  def __str__(self):
    return self.name
