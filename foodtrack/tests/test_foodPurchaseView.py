from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status

from foodtrack.models import PurchaseItem, UserPreference, FoodUsageCounter


class TestFoodPurchaseView(TestCase):
    fixtures = ['users.json', 'nutrients.json', 'food-categories.json', 'measure-units.json',
                'nutrient-derivations.json', 'food.json', 'food-portions.json', 'food-nutrients.json',
                'food-log-categories.json', 'currency.json']

    def setUp(self) -> None:
        self.client = Client()
        self.client.login(username="admin", password="admin")
        self.maxDiff = 10240

    def test_food_purchase_01(self):
        """Test simple call to food purchase view"""
        response = self.client.get(reverse("foodtrack-purchase"))
        self.assertTrue(status.is_success(response.status_code))

    def test_food_purchase_02(self):
        """Test that all user preferences are preserved in backend after a purchase is logged."""
        response = self.client.post(reverse("foodtrack-purchase"), data={
            "kind": "10",
            "store_name": "TEST",
            "pcs": "1",
            "food-id": "170457",
            "description": "test",
            "amount": ".5",
            "unit": "99999",
            "cost": "19.95",
            "currency": "1",
            "dt": "2019-08-12"
        })
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, reverse("foodtrack-purchase"))
        purchase = PurchaseItem.objects.filter(store_name="TEST")
        self.assertEqual(1, purchase.count())

        preference = get_object_or_404(UserPreference, owner_id=1)
        self.assertEqual("TEST", preference.prefs["forms"]["foodpurchaseform"]["store_name"])
        self.assertEqual(1, preference.prefs["forms"]["foodpurchaseform"]["currency"])
        self.assertEqual(99999, preference.prefs["forms"]["foodpurchaseform"]["unit"])
        self.assertEqual("2019-08-12", preference.prefs["forms"]["foodpurchaseform"]["dt"])

        usage_counter = get_object_or_404(FoodUsageCounter, owner_id=1, food_id=170457)
        self.assertEqual(1, usage_counter.count)

    def test_food_purchase_03(self):
        """Test for purchase form submission with POST, then response of the same form, but with user preferred
        defaults kept."""
        response = self.client.post(reverse("foodtrack-purchase"), data={
            "kind": "10",
            "store_name": "TEST",
            "pcs": "1",
            "food-id": "170457",
            "description": "test",
            "amount": ".5",
            "unit": "99999",
            "cost": "19.95",
            "currency": "1",
            "dt": "2019-08-12"
        })
        # self.assertEqual("", response.content.decode("utf-8"))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, reverse("foodtrack-purchase"))
        purchase = PurchaseItem.objects.filter(store_name="TEST", food_id=170457)
        self.assertEqual(1, purchase.count())

        response: TemplateResponse = self.client.get(reverse("foodtrack-purchase"))
        html = response.content.decode("utf-8")
        # self.assertEqual("", html)
        self.assertNotEqual(-1, html.find('<option value="99999" selected>kg</option>'))
        self.assertNotEqual(-1, html.find('name="store_name" value="TEST"'))
