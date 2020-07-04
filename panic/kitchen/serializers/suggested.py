"""Serializer for the SuggestedItem Model"""

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from ..models.suggested import SuggestedItem


class SuggestedItemSerializer(serializers.ModelSerializer):
  """Serializer for SuggestedItem"""
  name = serializers.CharField(
      max_length=255,
      validators=[UniqueValidator(queryset=SuggestedItem.objects.all())])

  class Meta:
    model = SuggestedItem
    fields = "__all__"
    read_only_fields = ("id",)
