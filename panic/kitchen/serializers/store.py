"""Serializer for the Store Model"""

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from ..models.store import Store


class StoreSerializer(serializers.ModelSerializer):
  """Serializer for Store"""
  user = serializers.HiddenField(default=serializers.CurrentUserDefault())

  class Meta:
    model = Store
    fields = "__all__"
    read_only_fields = ("id",)
    validators = [
        UniqueTogetherValidator(queryset=Store.objects.all(),
                                fields=['user', 'name'])
    ]
