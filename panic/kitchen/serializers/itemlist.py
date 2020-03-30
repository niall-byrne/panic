"""Serializer for the ItemList Model"""

from rest_framework import serializers

from ..models.itemlist import ItemList


class ItemListSerializer(serializers.ModelSerializer):
  """Serializer for ItemList"""

  class Meta:
    model = ItemList
    fields = "__all__"
    read_only_fields = ("id",)
