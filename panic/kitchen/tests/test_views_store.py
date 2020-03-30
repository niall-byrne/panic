"""Test the Store API."""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from ..models.store import Store
from ..serializers.store import StoreSerializer

SHELF_URL = reverse("kitchen:store-list")


class PublicStoreTest(TestCase):
  """Test the public Store API"""

  def setUp(self) -> None:
    self.client = APIClient()

  def test_login_required(self):
    """Test that login is required for retrieving shelves."""
    res = self.client.get(SHELF_URL)

    self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

  def test_create_login_required(self):
    payload = {"name": "Loblaws"}
    res = self.client.post(SHELF_URL, payload)

    self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


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

  def test_retrieve_shelves(self):
    """Test retrieving a list of stores."""
    self.sample_store(name="No Frills")
    self.sample_store(name="Loblaws")

    res = self.client.get(SHELF_URL)

    shelves = Store.objects.all().order_by("-name")
    serializer = StoreSerializer(shelves, many=True)

    assert len(shelves) == 2
    self.assertEqual(res.status_code, status.HTTP_200_OK)
    self.assertEqual(res.data, serializer.data)

  def test_delete_store(self):
    """Test deleting a store."""
    delete = self.sample_store(name="A&P")
    self.sample_store(name="Beckers")

    res_delete = self.client.delete(SHELF_URL + str(delete.id) + '/')
    res_get = self.client.get(SHELF_URL)

    shelves = Store.objects.all().order_by("-name")
    serializer = StoreSerializer(shelves, many=True)

    assert len(shelves) == 1
    self.assertEqual(res_delete.status_code, status.HTTP_204_NO_CONTENT)
    self.assertEqual(res_get.status_code, status.HTTP_200_OK)
    self.assertEqual(res_get.data, serializer.data)

  def test_create_store(self):
    """Test creating a store."""
    data = {"name": "Shoppers Drugmart"}

    res = self.client.post(SHELF_URL, data=data)

    shelves = Store.objects.all().order_by("-name")

    assert len(shelves) == 1
    self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    self.assertEqual(shelves[0].name, data['name'])
