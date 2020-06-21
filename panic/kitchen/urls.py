"""Kitchen App Urls"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = "kitchen"

router = DefaultRouter()
router.register("allitems", views.ListItemsViewSet, basename="allitems")
router.register("shelf", views.ShelfViewSet, basename="shelf")
router.register("store", views.StoreViewSet, basename="store")
router.register("item", views.ItemViewSet, basename="item")
router.register("transaction", views.TransactionViewSet, basename="transaction")

urlpatterns = [
    path("transaction_query/<int:item>/",
         views.TransactionQueryableViewSet.as_view(),
         name="transaction-query"),
    path("", include(router.urls))
]
