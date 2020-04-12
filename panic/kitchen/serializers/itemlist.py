"""Serializer for the ItemList Model"""

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from ..models.itemlist import ItemList


class ItemListSerializer(serializers.ModelSerializer):
  """Serializer for ItemList"""
  name = serializers.CharField(
      max_length=255,
      validators=[UniqueValidator(queryset=ItemList.objects.all())])

  class Meta:
    model = ItemList
    fields = "__all__"
    read_only_fields = ("id",)
