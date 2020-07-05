"""Test the Store API."""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils.http import urlencode
from rest_framework import status
from rest_framework.test import APIClient

from ..models.store import Store
from ..serializers.store import StoreSerializer

STORE_URL = reverse("kitchen:store-list")


def store_url_with_params(query_kwargs):
  return '{}?{}'.format(STORE_URL, urlencode(query_kwargs))


class PublicStoreTest(TestCase):
  """Test the public Store API"""

  def setUp(self) -> None:
    self.client = APIClient()

  def test_login_required(self):
    """Test that login is required for retrieving shelves."""
    res = self.client.get(STORE_URL)

    self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

  def test_create_login_required(self):
    payload = {"name": "Loblaws"}
    res = self.client.post(STORE_URL, payload)

    self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateStoreTest(TestCase):
  """Test the authorized Store API"""

  def sample_store(self, user=None, name="No Frills"):
    """Create a test store."""
    if user is None:
      user = self.user
    store = Store.objects.create(user=user, name=name)
    self.objects.append(store)
    return store

  @classmethod
  def setUpTestData(cls):
    cls.objects = list()
    cls.user = get_user_model().objects.create_user(
        username="testuser",
        email="test@niallbyrne.ca",
        password="test123",
    )
    cls.serializer = StoreSerializer
    cls.fields = {"name": 255}

  def setUp(self):
    self.objects = list()
    self.client = APIClient()
    self.client.force_authenticate(self.user)

  def tearDown(self) -> None:
    for obj in self.objects:
      obj.delete()

  def test_list_stores(self):
    """Test retrieving a list of stores."""
    self.sample_store(name="No Frills")
    self.sample_store(name="Loblaws")

    res = self.client.get(STORE_URL)

    shelves = Store.objects.all().order_by("index")
    serializer = StoreSerializer(shelves, many=True)

    assert len(shelves) == 2
    self.assertEqual(res.status_code, status.HTTP_200_OK)
    self.assertEqual(res.data['results'], serializer.data)

  def test_list_stores_paginated_correctly(self):
    """Test that retrieving a list of stores is limited correctly."""
    for index in range(0, 11):
      data = "storename" + str(index)
      self.sample_store(name=data)

    res = self.client.get(store_url_with_params({"page_size": 10}))
    self.assertEqual(len(res.data['results']), 10)
    self.assertIsNotNone(res.data['next'])
    self.assertIsNone(res.data['previous'])

  def test_delete_store(self):
    """Test deleting a store."""
    delete = self.sample_store(name="A&P")
    self.sample_store(name="Beckers")

    res_delete = self.client.delete(STORE_URL + str(delete.id) + '/')
    res_get = self.client.get(STORE_URL)

    shelves = Store.objects.all().order_by("index")
    serializer = StoreSerializer(shelves, many=True)

    assert len(shelves) == 1
    self.assertEqual(res_delete.status_code, status.HTTP_204_NO_CONTENT)
    self.assertEqual(res_get.status_code, status.HTTP_200_OK)
    self.assertEqual(res_get.data['results'], serializer.data)

  def test_create_store(self):
    """Test creating a store."""
    data = {"name": "Shoppers Drugmart"}

    res = self.client.post(STORE_URL, data=data)

    shelves = Store.objects.all().order_by("index")

    assert len(shelves) == 1
    self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    self.assertEqual(shelves[0].name, data['name'])
