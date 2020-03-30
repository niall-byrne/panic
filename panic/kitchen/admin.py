"""Kitchen Admin Models"""

from django.contrib import admin

from .models.itemlist import ItemList
from .models.shelf import Shelf
from .models.store import Store

admin.site.register(ItemList)
admin.site.register(Shelf)
admin.site.register(Store)
