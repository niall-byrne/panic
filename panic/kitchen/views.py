"""Kitchen App Views"""

from rest_framework import mixins, viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

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

AUTHENTICATION = (SessionAuthentication,)
PERMISSION = (IsAuthenticated,)


class ListItemsViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
  """List Items AutoCompletion View"""
  serializer_class = ItemListSerializer
  queryset = ItemList.objects.all()
  authentication_classes = AUTHENTICATION
  permission_classes = PERMISSION

  def get_queryset(self):
    return self.queryset.order_by("-name")


class ShelfViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
  """Shelf API View"""
  serializer_class = ShelfSerializer
  queryset = Shelf.objects.all()
  authentication_classes = (SessionAuthentication,)
  permission_classes = (IsAuthenticated,)

  def get_queryset(self):
    queryset = self.queryset.order_by("-name")
    return queryset.filter(user=self.request.user)

  def perform_create(self, serializer):
    """Create a new Shelf+"""
    serializer.save(user=self.request.user)


class StoreViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
  """Store API View"""
  serializer_class = StoreSerializer
  queryset = Store.objects.all()
  authentication_classes = AUTHENTICATION
  permission_classes = PERMISSION

  def get_queryset(self):
    queryset = self.queryset.order_by("-name")
    return queryset.filter(user=self.request.user)

  def perform_create(self, serializer):
    """Create a new Store"""
    serializer.save(user=self.request.user)


class ItemViewSet(
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
  authentication_classes = AUTHENTICATION
  permission_classes = PERMISSION

  def get_queryset(self):
    queryset = self.queryset.order_by("-name")
    return queryset.filter(user=self.request.user)

  def perform_create(self, serializer):
    """Create a new Item"""
    serializer.save(user=self.request.user)

  def perform_update(self, serializer):
    """Update a Item"""
    serializer.save(user=self.request.user)


class TransactionViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
  """Transaction API View"""
  serializer_class = TransactionSerializer
  queryset = Transaction.objects.all()
  authentication_classes = AUTHENTICATION
  permission_classes = PERMISSION

  def perform_create(self, serializer):
    """Create a new Transaction"""
    serializer.save(user=self.request.user)
