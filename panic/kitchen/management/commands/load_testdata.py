"""Loads Test Data into the Database"""

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand

from ...models.item import Item
from ...models.shelf import Shelf
from ...models.store import Store

DATA_PRESETS = {
    'storename': 'TestStore1',
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

    store = Store.objects.create(user=user, name=DATA_PRESETS['storename'])
    shelf = Shelf.objects.create(user=user, name=DATA_PRESETS['shelfname'])
    items = []
    for i in range(0, DATA_PRESETS['number_of_items']):
      new = Item(name=DATA_PRESETS['itemname'] + str(i),
                 user=user,
                 shelf_life="99",
                 shelf=shelf,
                 price="2.00",
                 quantity=20)
      items.append(new)

    for item in Item.objects.bulk_create(items):
      item.preferred_stores.add(store)
      item.save()
