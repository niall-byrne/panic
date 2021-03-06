"""A variation on django-bleach BleachField, derived from CharField"""

from django.conf import settings
from django.db import models
from django_bleach.models import BleachField


class BlondeCharField(models.CharField, BleachField):
  """A django_bleach derived char field, with appropriate protection."""

  def pre_save(self, model_instance, add):
    """Overrides the default :func:`django.db.models.fields.pre_save` behavior
    to allow for restoring some modified fields after they have been "bleached".
    """
    restored_data = None
    data = super(BlondeCharField, self).pre_save(model_instance, add)
    for key, value in getattr(settings, "BLEACH_RESTORE_LIST", {}).items():
      restored_data = data.replace(key, value)
    if restored_data:
      setattr(model_instance, self.attname, restored_data)
      return restored_data
    return data
