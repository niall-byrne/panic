"""Loads Test Data into the Database"""

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand

from kitchen.models.item import Item
from kitchen.models.shelf import Shelf
from kitchen.models.store import Store

DATA_PRESETS = {
    'storename': 'TestStore',
    'shelfname': 'TestShelf1',
    'itemname': 'TestItem',
    'number_of_items': 200
}


class Command(BaseCommand):
  """Django command that loads data for functional testing."""
  help = 'Loads sets of pre-defined test data into the database'

  def add_arguments(self, parser):
    parser.add_argument(
        'user',
        nargs=1,
        type=str,
    )

  def handle(self, *args, **options):
    """Handle the command"""
    try:
      user = get_user_model().objects.get(username=options['user'][0])
    except ObjectDoesNotExist:
      self.stderr.write(self.style.ERROR('The specified user does not exist.'))
      return

    shelf = Shelf.objects.create(user=user, name=DATA_PRESETS['shelfname'])
    items = []
    stores = []
    for i in range(0, DATA_PRESETS['number_of_items']):
      new_item = Item(name=DATA_PRESETS['itemname'] + str(i),
                      user=user,
                      shelf_life="99",
                      shelf=shelf,
                      price="2.00",
                      quantity=20)
      new_store = Store(user=user, name=DATA_PRESETS['storename'] + str(i))
      items.append(new_item)
      stores.append(new_store)

    for store in Store.objects.bulk_create(stores):
      store.save()

    for item in Item.objects.bulk_create(items):
      item.preferred_stores.add(stores[0])
      item.save()
