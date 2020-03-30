"""Test the ItemList Serializer."""

from django.test import TestCase
from rest_framework.serializers import ValidationError

from ..models.itemlist import ItemList
from ..serializers.itemlist import ItemListSerializer


class TestItemList(TestCase):

  def sample_item(self, name="Red Beans"):
    """Create a test item."""
    item = ItemList.objects.create(name=name)
    self.objects.append(item)
    return item

  @staticmethod
  def generate_overload(fields):
    return_list = []
    for key, value in fields.items():
      overloaded = dict()
      overloaded[key] = "abc" * value
      return_list.append(overloaded)
    return return_list

  @classmethod
  def setUpTestData(cls):
    cls.objects = list()
    cls.serializer = ItemListSerializer
    cls.fields = {"name": 255}

  def setUp(self):
    self.objects = list()

  def tearDown(self) -> None:
    for obj in self.objects:
      obj.delete()

  def testDeserialize(self):
    test_value = "Custard"
    item = self.sample_item(test_value)

    serialized = self.serializer(item)

    self.assertDictEqual(serialized.data, {'id': 3, 'name': 'Custard'})

  def testSerialize(self):
    test_value = {"name": "Grape"}
    serialized = self.serializer(data=test_value)
    serialized.is_valid()

    self.assertEqual(serialized.data['name'], test_value['name'])

  def testFieldLengths(self):
    overloads = self.generate_overload(self.fields)
    for overload in overloads:
      with self.assertRaises(ValidationError):
        serialized = self.serializer(data=overload)
        serialized.is_valid(raise_exception=True)
