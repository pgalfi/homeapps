from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status

from foodtrack import constants
from foodtrack.models import Currency


class TestFoodPurchasesSummary(TestCase):
    fixtures = ['users.json', 'nutrients.json', 'food-categories.json', 'measure-units.json', 'food.json',
                'currency.json', 'purchase-items.json']

    def setUp(self) -> None:
        self.client = Client()
        self.client.login(username="admin", password="admin")
        self.maxDiff = 10240

    def test_food_purchase_summary_01(self):
        response = self.client.get(reverse("foodtrack-purchase-summary"))
        self.assertTrue(status.is_success(response.status_code))

    def test_food_purchase_summary_02(self):
        response = self.client.get(reverse("foodtrack-purchase-summary") + "?store_name=TEST")
        self.assertEqual(1, response.content.decode("utf-8").count("TEST"))

    def test_food_purchase_summary_03(self):
        test_currency1 = Currency.objects.filter(pk=1)
        self.assertEqual(1, test_currency1.count())
        response = self.client.get(reverse("foodtrack-purchase-summary") + "?store_name=TEST&summary_type=" +
                                   str(constants.FOOD_PURCHASE_SUMM_STORE) + "&currency_id=1")
        self.assertEqual(2, response.content.decode("utf-8").count("TEST"))

    def test_food_purchase_summary_04(self):
        response = self.client.get(reverse("foodtrack-purchase-summary") + "?store_name=TEST&summary_type=" +
                                   str(constants.FOOD_PURCHASE_SUMM_STORE_ITEM) + "&currency_id=2")
        response_content = response.content.decode("utf-8")
        self.assertEqual(3, response_content.count("TEST"))
        self.assertNotEqual(-1, response_content.find("5.9 USD"))
        self.assertNotEqual(-1, response_content.find("1.5 USD"))



