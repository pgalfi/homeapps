from django.test import TestCase, Client
from django.urls import reverse


class TestFoodPurchaseList(TestCase):

    fixtures = ['users.json', 'nutrients.json', 'food-categories.json', 'measure-units.json', 'food.json',
                'currency.json', 'purchase-items.json']

    def setUp(self):
        self.client = Client()
        self.client.login(username="admin", password="admin")
        self.maxDiff = 10240

    def test_purchase_list_01(self):
        response = self.client.get(reverse("foodtrack-purchase-list"))
        self.assertEqual(2, response.content.decode("utf-8").count("<tr"))

    def test_purchase_list_02(self):
        response = self.client.get(reverse("foodtrack-purchase-list") + "?food_id=170457")
        self.assertEqual(1, response.content.decode("utf-8").count("<tr"))

    def test_purchase_list_03(self):
        response = self.client.get(reverse("foodtrack-purchase-list") + "?dt_start=2019-08-18")
        self.assertEqual(0, response.content.decode("utf-8").count("<tr"))

    def test_purchase_list_04(self):
        response = self.client.get(reverse("foodtrack-purchase-list") + "?dt_end=2019-08-18")
        self.assertEqual(2, response.content.decode("utf-8").count("<tr"))

    def test_purchase_list_05(self):
        response = self.client.get(reverse("foodtrack-purchase-list") + "?store_name=TEST")
        self.assertEqual(2, response.content.decode("utf-8").count("<tr"))

