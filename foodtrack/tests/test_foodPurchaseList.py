from django.test import TestCase, Client
from django.urls import reverse


class TestFoodPurchaseList(TestCase):

    fixtures = ['users.json', 'nutrients.json', 'food-categories.json', 'measure-units.json', 'food.json',
                'currency.json', 'purchase-items.json']

    def setUp(self):
        self.client = Client()
        self.client.login(username="admin", password="admin")

    def test_purchase_list_01(self):
        response = self.client.get(reverse("foodtrack-purchase-list"))
        self.maxDiff = 10240
        self.assertEqual("", response.content.decode("utf-8"))

