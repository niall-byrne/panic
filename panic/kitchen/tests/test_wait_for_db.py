from io import StringIO
from unittest.mock import patch

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase


class CommandTests(TestCase):

  def test_wait_for_db_ready(self):
    """Test waiting for db when db is available."""

    capture = StringIO()

    with patch("django.db.connection.ensure_connection") as cn:
      cn.return_value = True
      call_command("wait_for_db", stdout=capture)
      self.assertEqual(cn.call_count, 1)

  @patch("time.sleep", return_value=True)
  def test_wait_for_db(self, ts):
    """Test waiting for db"""

    capture = StringIO()

    with patch("django.db.connection.ensure_connection") as cn:
      cn.side_effect = [OperationalError] * 5 + [True]
      call_command("wait_for_db", stdout=capture)
      self.assertEqual(cn.call_count, 6)
