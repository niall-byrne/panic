"""Serializer for the Store Model"""

from rest_framework import serializers

from ..models.store import Store


class StoreSerializer(serializers.ModelSerializer):
  """Serializer for Store"""
  user = serializers.HiddenField(default=serializers.CurrentUserDefault())

  class Meta:
    model = Store
    fields = ("id", "user", "name")
    read_only_fields = ("id",)
