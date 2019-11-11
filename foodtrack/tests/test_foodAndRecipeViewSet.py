from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient


class TestFoodAndRecipeViewSet(TestCase):

    fixtures = ['users.json', 'nutrients.json', 'food-categories.json', 'measure-units.json',
                'nutrient-derivations.json', 'food.json', 'food-portions.json', 'food-nutrients.json',
                'recipes.json']

    def setUp(self) -> None:
        self.client = APIClient()
        self.maxDiff = 4096

    def test_foodandrecipe_01(self):
        response:Response = self.client.get(reverse("foodandrecipe-list", args=["v1"]), format="json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(3, len(response.data["results"]))

    def test_foodandrecipe_02(self):
        response: Response = self.client.get(reverse("foodandrecipe-list", args=["v1"]) + "?search=tomato", format="json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(2, len(response.data["results"]))
