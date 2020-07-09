"""Serializer for the Item Model"""

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from ..models.item import Item
from . import DUPLICATE_OBJECT_MESSAGE


class ItemSerializer(serializers.ModelSerializer):
  """Serializer for Item"""
  user = serializers.HiddenField(default=serializers.CurrentUserDefault())

  class Meta:
    model = Item
    exclude = ('index',)
    read_only_fields = (
        "id",
        "next_expiry_date",
        "next_expiry_quantity",
        "expired",
    )
    validators = [
        UniqueTogetherValidator(queryset=Item.objects.all(),
                                fields=['user', 'name'],
                                message=DUPLICATE_OBJECT_MESSAGE)
    ]
