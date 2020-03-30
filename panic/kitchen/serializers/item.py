"""Serializer for the Item Model"""

from rest_framework import serializers

from ..models.item import Item


class ItemSerializer(serializers.ModelSerializer):
  """Serializer for Item"""
  user = serializers.HiddenField(default=serializers.CurrentUserDefault())

  class Meta:
    model = Item
    fields = "__all__"
    read_only_fields = ("id",)
