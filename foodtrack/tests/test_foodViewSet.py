from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


class TestFoodViewSet(TestCase):

    fixtures = ['users.json', 'nutrients.json', 'food-categories.json', 'measure-units.json',
                'nutrient-derivations.json', 'food.json', 'food-portions.json', 'food-nutrients.json']

    def setUp(self) -> None:
        self.client = APIClient()
        self.endpoint = reverse("food-list", args=["v1"])
        self.maxDiff = 4096

    def test_getfood_list(self):
        response = self.client.get(self.endpoint)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_getfood_list_01(self):
        response = self.client.get(self.endpoint + "?description=tomato", format="json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(1, len(response.data["results"]))
        self.assertEqual(11, response.data["results"][0]["category"]["id"])

    def test_getfood_list_02(self):
        response = self.client.get(self.endpoint + "?description=tomato&category=11", format="json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(1, len(response.data["results"]))
        self.assertEqual(11, response.data["results"][0]["category"]["id"])

