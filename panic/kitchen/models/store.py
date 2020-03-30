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
