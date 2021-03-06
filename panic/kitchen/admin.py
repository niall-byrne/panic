"""Kitchen Admin Models"""

from django.contrib import admin

from .models.item import Item
from .models.shelf import Shelf
from .models.store import Store
from .models.suggested import SuggestedItem
from .models.transaction import Transaction

admin.site.register(Item)
admin.site.register(SuggestedItem)
admin.site.register(Shelf)
admin.site.register(Store)
admin.site.register(Transaction)
