"""A Bleach Field Derived form Char Field"""

from django.db import models

from bleach import clean

from django_bleach.utils import get_bleach_default_options


class BlondeCharField(models.CharField):
    """Derived from CharField, rather than TextField"""
    def __init__(self, allowed_tags=None, allowed_attributes=None,
                 allowed_styles=None, allowed_protocols=None,
                 strip_tags=None, strip_comments=None, *args, **kwargs):

        super(BlondeCharField, self).__init__(*args, **kwargs)

        self.bleach_kwargs = get_bleach_default_options()

        if allowed_tags:
            self.bleach_kwargs['tags'] = allowed_tags
        if allowed_attributes:
            self.bleach_kwargs['attributes'] = allowed_attributes
        if allowed_styles:
            self.bleach_kwargs['styles'] = allowed_styles
        if allowed_protocols:
            self.bleach_kwargs['protocols'] = allowed_protocols
        if strip_tags:
            self.bleach_kwargs['strip'] = strip_tags
        if strip_comments:
            self.bleach_kwargs['strip_comments'] = strip_comments

    def pre_save(self, model_instance, add):
        data = getattr(model_instance, self.attname)
        if data:
            clean_value = clean(
                data,
                **self.bleach_kwargs
            )
            setattr(model_instance, self.attname, clean_value)
            return clean_value
        return data
