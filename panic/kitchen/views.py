"""Kitchen App Views"""

import datetime

from django.conf import settings
from django.utils import timezone
from django_filters import rest_framework as filters
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, viewsets

from spa_security.auth_cookie import CSRFMixin
from .filters import ItemFilter, TransactionFilter
from .models.item import Item
from .models.shelf import Shelf
from .models.store import Store
from .models.suggested import SuggestedItem
from .models.transaction import Transaction
from .pagination import PagePagination, PagePaginationWithOverride
from .serializers.item import ItemSerializer
from .serializers.shelf import ShelfSerializer
from .serializers.store import StoreSerializer
from .serializers.suggested import SuggestedItemSerializer
from .serializers.transaction import TransactionSerializer
from .swagger import openapi_ready


class SuggestedItemViewSet(
    CSRFMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
  """Suggested Items List View"""
  serializer_class = SuggestedItemSerializer
  queryset = SuggestedItem.objects.all().order_by("name")
  pagination_class = PagePagination

  @openapi_ready
  def get_queryset(self):
    queryset = self.queryset
    return queryset.order_by("name")


class ShelfViewSet(
    CSRFMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
  """Shelf API View"""
  serializer_class = ShelfSerializer
  queryset = Shelf.objects.all()
  pagination_class = PagePaginationWithOverride

  @openapi_ready
  def get_queryset(self):
    queryset = self.queryset
    return queryset.filter(user=self.request.user).order_by("index")

  @openapi_ready
  def perform_create(self, serializer):
    """Create a new Shelf"""
    serializer.save(user=self.request.user)


class StoreViewSet(
    CSRFMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
  """Store API View"""
  serializer_class = StoreSerializer
  queryset = Store.objects.all()
  pagination_class = PagePaginationWithOverride

  @openapi_ready
  def get_queryset(self):
    queryset = self.queryset
    return queryset.filter(user=self.request.user).order_by("index")

  @openapi_ready
  def perform_create(self, serializer):
    """Create a new Store"""
    serializer.save(user=self.request.user)


class ItemViewSet(
    CSRFMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
  """Item API View"""
  serializer_class = ItemSerializer
  queryset = Item.objects.all()
  filter_backends = (filters.DjangoFilterBackend,)
  filterset_class = ItemFilter
  pagination_class = PagePagination

  @openapi_ready
  def get_queryset(self):
    queryset = self.queryset
    return queryset.filter(user=self.request.user).order_by("index")

  @openapi_ready
  def perform_create(self, serializer):
    """Create a new Item"""
    serializer.save(user=self.request.user)

  @openapi_ready
  def perform_update(self, serializer):
    """Update a Item"""
    serializer.save(user=self.request.user)


custom_transaction_view_parm = openapi.Parameter(
    'history',
    openapi.IN_QUERY,
    description="the number of days to retrieve history for",
    type=openapi.TYPE_STRING,
    default=14
)


class TransactionViewSet(
    CSRFMixin,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
  """Transaction API View"""
  serializer_class = TransactionSerializer
  queryset = Transaction.objects.all()
  filter_backends = (filters.DjangoFilterBackend,)
  filterset_class = TransactionFilter

  def parse_history_querystring(self):
    try:
      return int(
          self.request.GET.get('history', settings.TRANSACTION_HISTORY_MAX)
      )
    except ValueError:
      return int(settings.TRANSACTION_HISTORY_MAX)

  @swagger_auto_schema(manual_parameters=[custom_transaction_view_parm])
  def list(self, request, *args, **kwargs):
    return super().list(request, *args, **kwargs)

  @openapi_ready
  def get_queryset(self):
    history = self.parse_history_querystring()

    queryset = self.queryset
    return queryset.\
        filter(user=self.request.user).\
        filter(
          datetime__lte=timezone.now(),
          datetime__gt=timezone.now() - datetime.timedelta(days=int(history))
        ).\
        order_by('-datetime')

  @openapi_ready
  def perform_create(self, serializer):
    """Create a new Transaction"""
    serializer.save(user=self.request.user)
