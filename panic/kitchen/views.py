"""Kitchen App Views"""

from django.conf import settings
from django_filters import rest_framework as filters
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, viewsets
from rest_framework.response import Response

from spa_security.auth_cookie import CSRFMixin
from .filters import ItemFilter
from .models.item import Item
from .models.itemlist import ItemList
from .models.shelf import Shelf
from .models.store import Store
from .models.transaction import Transaction
from .serializers.item import ItemSerializer
from .serializers.itemlist import ItemListSerializer
from .serializers.shelf import ShelfSerializer
from .serializers.store import StoreSerializer
from .serializers.transaction import TransactionSerializer
from .swagger import openapi_ready


class ListItemsViewSet(
    CSRFMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
  """List Items AutoCompletion View"""
  serializer_class = ItemListSerializer
  queryset = ItemList.objects.all()

  @openapi_ready
  def get_queryset(self):
    return self.queryset.order_by("-name")


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

  @openapi_ready
  def get_queryset(self):
    queryset = self.queryset.order_by("-name")
    return queryset.filter(user=self.request.user)

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

  @openapi_ready
  def get_queryset(self):
    queryset = self.queryset.order_by("-name")
    return queryset.filter(user=self.request.user)

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

  @openapi_ready
  def get_queryset(self):
    queryset = self.queryset.order_by("-name")
    return queryset.filter(user=self.request.user)

  @openapi_ready
  def perform_create(self, serializer):
    """Create a new Item"""
    serializer.save(user=self.request.user)

  @openapi_ready
  def perform_update(self, serializer):
    """Update a Item"""
    serializer.save(user=self.request.user)


custom_transaction_view_parm = openapi.Parameter(
    'id',
    openapi.IN_PATH,
    description="the item id to find transactions for",
    type=openapi.TYPE_INTEGER,
)


class TransactionViewSet(
    CSRFMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
  """Transaction API View"""
  serializer_class = TransactionSerializer
  queryset = Transaction.objects.all()

  @openapi_ready
  def get_queryset(self):
    item = self.kwargs['pk']
    queryset = self.queryset.order_by("-date")
    return queryset.filter(user=self.request.user, item=item)

  @openapi_ready
  def perform_create(self, serializer):
    """Create a new Transaction"""
    serializer.save(user=self.request.user)

  @openapi_ready
  @swagger_auto_schema(manual_parameters=[custom_transaction_view_parm],
                       responses={200: TransactionSerializer(many=True)})
  def retrieve(self, request, *args, **kwargs):  # pylint: disable=W0613
    """Retrieve transactions by Item."""
    queryset = self.get_queryset()[:settings.MAXIMUM_TRANSACTIONS]
    serializer = self.get_serializer(queryset, many=True)
    return Response(serializer.data)
