"""User Shelf Model"""

from django.contrib.auth import get_user_model
from django.db import models

from spa_security.fields import BlondeCharField

User = get_user_model()


class Shelf(models.Model):
  """User Shelf Model"""
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  name = BlondeCharField(max_length=255)

  class Meta:
    constraints = [
        models.UniqueConstraint(fields=['user', 'name'], name='shelf per user')
    ]

  def __str__(self):
    return str(self.name)

  # pylint: disable=W0222
  def save(self, *args, **kwargs):
    self.full_clean()
    return super(Shelf, self).save(*args, **kwargs)
