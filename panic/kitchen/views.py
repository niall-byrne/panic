"""Kitchen App Views"""

from rest_framework import mixins, viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models.itemlist import ItemList
from .serializers.itemlist import ItemListSerializer


class ListItemsViewSet(viewsets.ViewSet, mixins.ListModelMixin):
  """List Items AutoCompletion View"""

  authentication_classes = (BasicAuthentication,)
  permission_classes = (IsAuthenticated,)
  queryset = ItemList.objects.all()

  def get_queryset(self):
    return self.queryset.order_by("-name")

  def list(self, request, *args, **kwargs):
    queryset = self.get_queryset()
    serializer = ItemListSerializer(queryset, many=True)
    return Response(serializer.data)
