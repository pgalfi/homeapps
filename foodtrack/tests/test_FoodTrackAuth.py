from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status


class TestFoodTrackAuth(TestCase):
    fixtures = ['users.json', ]

    def setUp(self) -> None:
        self.client = Client()

    def test_food_purchase_noauth(self):
        response = self.client.get(reverse("foodtrack-index"))
        self.assertRedirects(response, reverse("foodtrack-login") + "?next=" + reverse("foodtrack-index"))

    def test_authenticate(self):
        response = self.client.post(reverse("foodtrack-login"), {"username": "admin", "password": "admin"})
        self.assertRedirects(response, reverse("foodtrack-index"), fetch_redirect_response=False)

