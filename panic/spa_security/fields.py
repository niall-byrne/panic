"""A variation on django-bleach BleachField, derived from CharField"""

from django.db import models
from django_bleach.models import BleachField


class BlondeCharField(models.CharField, BleachField):
  pass
