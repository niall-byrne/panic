"""Kitchen App Views"""

from rest_framework import mixins, viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models.itemlist import ItemList
from .models.shelf import Shelf
from .serializers.itemlist import ItemListSerializer
from .serializers.shelf import ShelfSerializer
from .models.store import Store
from .serializers.store import StoreSerializer


class ListItemsViewSet(
    viewsets.ViewSet,
    mixins.ListModelMixin,
):
  """List Items AutoCompletion View"""

  authentication_classes = (SessionAuthentication,)
  permission_classes = (IsAuthenticated,)
  queryset = ItemList.objects.all()

  def get_queryset(self):
    return self.queryset.order_by("-name")

  def list(self, request, *args, **kwargs):
    queryset = self.get_queryset()
    serializer = ItemListSerializer(queryset, many=True)
    return Response(serializer.data)


class ShelfViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
  serializer_class = ShelfSerializer
  queryset = Shelf.objects.all()
  authentication_classes = (SessionAuthentication,)
  permission_classes = (IsAuthenticated,)

  def get_queryset(self):
    queryset = self.queryset.order_by("-name")
    return queryset.filter(user=self.request.user)

  def perform_create(self, serializer):
    """Create a new shelf"""
    serializer.save(user=self.request.user)


class StoreViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
  serializer_class = StoreSerializer
  queryset = Store.objects.all()
  authentication_classes = (SessionAuthentication,)
  permission_classes = (IsAuthenticated,)

  def get_queryset(self):
    queryset = self.queryset.order_by("-name")
    return queryset.filter(user=self.request.user)

  def perform_create(self, serializer):
    """Create a new shelf"""
    serializer.save(user=self.request.user)
