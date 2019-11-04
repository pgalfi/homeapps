from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status


class TestFoodPurchasesSummary(TestCase):
    fixtures = ['users.json', 'nutrients.json', 'food-categories.json', 'measure-units.json',
                'nutrient-derivations.json', 'food.json', 'food-portions.json', 'food-nutrients.json',
                'food-log-categories.json', 'currency.json']

    def setUp(self) -> None:
        self.client = Client()
        self.client.login(username="admin", password="admin")
        self.maxDiff = 10240

    def test_food_purchase_summary_01(self):
        """Test simple call to food purchase summary view"""
        response = self.client.get(reverse("foodtrack-purchase-summary"))
        self.assertTrue(status.is_server_error(response.status_code))


