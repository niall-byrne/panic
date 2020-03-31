"""Kitchen Admin Models"""

from django.contrib import admin

from .models.item import Item
from .models.itemlist import ItemList
from .models.shelf import Shelf
from .models.store import Store
from .models.transaction import Transaction

admin.site.register(Item)
admin.site.register(ItemList)
admin.site.register(Shelf)
admin.site.register(Store)
admin.site.register(Transaction)
