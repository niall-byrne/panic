"""Serializer for the Shelf Model"""

from rest_framework import serializers

from ..models.shelf import Shelf


class ShelfSerializer(serializers.ModelSerializer):
  """Serializer for Shelf"""
  user = serializers.HiddenField(default=serializers.CurrentUserDefault())

  class Meta:
    model = Shelf
    fields = '__all__'
    read_only_fields = ("id",)
