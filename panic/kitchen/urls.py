"""Kitchen App Urls"""

from django.urls import include, path
from rest_framework import routers

from . import views

app_name = "kitchen"

router = routers.SimpleRouter()
router.register(
    "suggested",
    views.SuggestedItemViewSet,
    basename="suggestions",
)
router.register("shelves", views.ShelfViewSet, basename="shelves")
router.register("stores", views.StoreViewSet, basename="stores")
router.register("items", views.ItemViewSet, basename="items")
router.register(
    "transactions",
    views.TransactionViewSet,
    basename="transactions",
)

urlpatterns = [
    path("", include(router.urls)),
]
