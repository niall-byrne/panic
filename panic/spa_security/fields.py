"""A variation on django-bleach BleachField, derived from CharField"""

from django.db import models
from django_bleach.models import BleachField


class BlondeCharField(models.CharField, BleachField):
  """A django_bleach derived char field, with appropriate protection."""
