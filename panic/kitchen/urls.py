"""Kitchen App Urls"""

from django.urls import include, path
from rest_framework import routers

from . import views

app_name = "kitchen"

router = routers.SimpleRouter()
router.register("suggested", views.SuggestedItemViewSet, basename="suggested")
router.register("shelf", views.ShelfViewSet, basename="shelf")
router.register("store", views.StoreViewSet, basename="store")
router.register("item", views.ItemViewSet, basename="item")
router.register("transaction", views.TransactionViewSet, basename="transaction")

urlpatterns = [
    path("", include(router.urls)),
]
