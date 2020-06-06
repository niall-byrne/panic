"""Filters for the Kitchen Application Views."""

from django_filters import rest_framework as filters

from .models.item import Item


class ItemFilter(filters.FilterSet):

  class Meta:
    model = Item
    fields = ['shelf', 'preferred_stores']
