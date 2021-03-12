from django.test import TestCase
from store.models import Category , Product
# Create your tests here.


class TestCategoryModel(TestCase):
    def setUp(self):
        self.data1 = Category.objects.create(name = "Test" , slug="test")


    def test_Categeory_model(self):
        data = self.data1
        self.assertTrue(isinstance(data , Category))

    def test_return_name_str(self):
        data = self.data1
        self.assertEqual(str(data) , "Test")


