"""Kitchen App Urls"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = "kitchen"

router = DefaultRouter()
router.register("allitems", views.ListItemsViewSet, basename="allitems")
router.register("shelf", views.ShelfViewSet, basename="shelf")
urlpatterns = [path("", include(router.urls))]
