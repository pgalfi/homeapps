from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status


class TestFoodPurchasesSummary(TestCase):
    fixtures = ['users.json', 'nutrients.json', 'food-categories.json', 'measure-units.json', 'food.json',
                'currency.json', 'purchase-items.json']

    def setUp(self) -> None:
        self.client = Client()
        self.client.login(username="admin", password="admin")
        self.maxDiff = 10240

    def test_food_purchase_summary_01(self):
        """Test simple call to food purchase summary view"""
        response = self.client.get(reverse("foodtrack-purchase-summary"))
        self.assertTrue(status.is_success(response.status_code))

    def test_food_purchase_summary_02(self):
        response = self.client.get(reverse("foodtrack-purchase-summary") + "?store_name=TEST")
        self.assertEqual(1, response.content.decode("utf-8").count("TEST"))

    def test_food_purchase_summary_03(self):
        response = self.client.get(reverse("foodtrack-purchase-summary") + "?store_name=TEST&summary_type=40&currency_id=1")
        self.assertEqual(2, response.content.decode("utf-8").count("TEST"))

    def test_food_purchase_summary_04(self):
        response = self.client.get(reverse("foodtrack-purchase-summary") + "?store_name=TEST&summary_type=40&currency_id=2")
        self.assertEqual(3, response.content.decode("utf-8").count("TEST"))


