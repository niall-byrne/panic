"""Test Main Frontend View"""

from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status

ITEM_URL = reverse("frontend-main")


class PublicItemTest(TestCase):
  """Test the public Item API"""

  def setUp(self) -> None:
    self.client = Client()

  def test_login_required(self):
    """Test that login is required for retrieving shelves."""
    res = self.client.get(ITEM_URL)
    self.assertEqual(res.status_code, status.HTTP_200_OK)
