"""Filters for the Kitchen Application Views."""

from django_filters import rest_framework as simple_filters

from .models.item import Item


class ItemFilter(simple_filters.FilterSet):

  class Meta:
    model = Item
    fields = ['shelf', 'preferred_stores']
