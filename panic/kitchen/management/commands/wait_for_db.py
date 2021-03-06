"""Admin Command to Wait for the Database to be Accessible"""

import time

from django.core.management.base import BaseCommand
from django.db import connection
from django.db.utils import OperationalError


class Command(BaseCommand):
  """Django command that waits for database to be available"""
  help = 'Pauses for database connectivity before proceeding.'

  def handle(self, *args, **options):
    """Handle the command"""
    self.stdout.write("Waiting for database...")
    while True:
      try:
        connection.ensure_connection()
        break
      except OperationalError:
        self.stdout.write("Database unavailable, waiting 1 second...")
        time.sleep(1)

    self.stdout.write(self.style.SUCCESS("Database available!"))
