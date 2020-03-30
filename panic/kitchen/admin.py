"""Kitchen Admin Models"""

from django.contrib import admin

from .models.itemlist import ItemList
from .models.shelf import Shelf

admin.site.register(ItemList)
admin.site.register(Shelf)
