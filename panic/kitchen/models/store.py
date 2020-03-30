"""User Stores Model"""

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Store(models.Model):
  """User Store Model"""
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  name = models.CharField(max_length=255)

  def __str__(self):
    return self.name

  # pylint: disable=W0221
  def save(self, *args, **kwargs):
    self.full_clean()
    return super(Store, self).save(*args, **kwargs)
