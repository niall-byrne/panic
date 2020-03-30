"""User Shelf Model"""

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Shelf(models.Model):
  """User Shelf Model"""
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  name = models.CharField(max_length=255)

  def __str__(self):
    return self.name
