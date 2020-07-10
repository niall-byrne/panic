"""Test the Shelf API."""

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils.http import urlencode
from rest_framework import status
from rest_framework.test import APIClient

from ..models.shelf import Shelf
from ..serializers.shelf import ShelfSerializer

SHELF_URL = reverse("kitchen:shelf-list")


def shelf_url_with_params(query_kwargs):
  return '{}?{}'.format(SHELF_URL, urlencode(query_kwargs))


class PublicShelfTest(TestCase):
  """Test the public Shelf API"""

  def setUp(self) -> None:
    self.client = APIClient()

  def test_login_required(self):
    """Test that login is required for retrieving shelves."""
    res = self.client.get(SHELF_URL)

    self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

  def test_create_login_required(self):
    payload = {"name": "Pantry"}
    res = self.client.post(SHELF_URL, payload)

    self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateShelfTest(TestCase):
  """Test the authorized Shelf API"""

  def sample_shelf(self, user=None, name="Over Sink"):
    """Create a test shelf."""
    if user is None:
      user = self.user
    shelf = Shelf.objects.create(user=user, name=name)
    self.objects.append(shelf)
    return shelf

  @classmethod
  def setUpTestData(cls):
    cls.objects = list()
    cls.user = get_user_model().objects.create_user(
        username="testuser",
        email="test@niallbyrne.ca",
        password="test123",
    )
    cls.serializer = ShelfSerializer
    cls.fields = {"name": 255}

  def setUp(self):
    self.objects = list()
    self.client = APIClient()
    self.client.force_authenticate(self.user)

  def tearDown(self) -> None:
    for obj in self.objects:
      obj.delete()

  def test_list_shelves(self):
    """Test retrieving a list of shelves."""
    self.sample_shelf(name="Refrigerator")
    self.sample_shelf(name="Pantry")

    res = self.client.get(SHELF_URL)

    shelves = Shelf.objects.all().order_by("index")
    serializer = ShelfSerializer(shelves, many=True)

    assert len(shelves) == 2
    self.assertEqual(res.status_code, status.HTTP_200_OK)
    self.assertEqual(res.data['results'], serializer.data)

  def test_list_shelves_paginated_correctly(self):
    """Test retrieving a list of shelves is paginated correctly."""
    for index in range(0, 11):
      data = 'shelfname' + str(index)
      self.sample_shelf(name=data)

    res = self.client.get(shelf_url_with_params({"page_size": 10}))
    self.assertEqual(len(res.data['results']), 10)
    self.assertIsNotNone(res.data['next'])
    self.assertIsNone(res.data['previous'])

  def test_list_shelves_paginated_overidden_correctly(self):
    """Test retrieving a the full list of shelves."""
    for index in range(0, 11):
      data = 'shelfname' + str(index)
      self.sample_shelf(name=data)

    res = self.client.get(
        shelf_url_with_params({
            "page_size": 10,
            settings.PAGINATION_OVERRIDE_PARAM: "true"
        }))
    self.assertEqual(len(res.data['results']), 11)
    self.assertIsNone(res.data['next'])
    self.assertIsNone(res.data['previous'])

  def test_delete_shelf(self):
    """Test deleting a shelf."""
    delete = self.sample_shelf(name="Refrigerator")
    self.sample_shelf(name="Pantry")

    res_delete = self.client.delete(SHELF_URL + str(delete.id) + '/')
    res_get = self.client.get(SHELF_URL)

    shelves = Shelf.objects.all().order_by("index")
    serializer = ShelfSerializer(shelves, many=True)

    assert len(shelves) == 1
    self.assertEqual(res_delete.status_code, status.HTTP_204_NO_CONTENT)
    self.assertEqual(res_get.status_code, status.HTTP_200_OK)
    self.assertEqual(res_get.data['results'], serializer.data)

  def test_create_shelf(self):
    """Test creating a shelf."""
    data = {"name": "Refrigerator"}

    res = self.client.post(SHELF_URL, data=data)

    shelves = Shelf.objects.all().order_by("index")

    assert len(shelves) == 1
    self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    self.assertEqual(shelves[0].name, data['name'])
